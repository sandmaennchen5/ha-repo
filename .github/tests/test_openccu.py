import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('sync_openccu', ROOT / '.github/scripts/sync_openccu.py')
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


class OpenCCUTests(unittest.TestCase):
    def test_config_format_and_defaults(self):
        import yaml
        original = {'arch': ['amd64'], 'ingress': False, 'apparmor': True, 'boot': 'auto'}
        normalized = sync.normalize_config(original)
        text = sync.dump_yaml(normalized).decode()
        self.assertIn('  - amd64', text)
        self.assertEqual(yaml.safe_load(text), {'arch': ['amd64']})
        nondefault = {'ingress': True, 'apparmor': False, 'boot': 'manual'}
        self.assertEqual(sync.normalize_config(nondefault), nondefault)

    def test_stable_and_modern_backports(self):
        for baseline, name in [('stable', 'ha-proxy.js'), ('modern', 'ha-proxy.js'), ('modern', 'ha-proxy.js.gtpl')]:
            source = (sync.PATCH / baseline / name).read_text().encode()
            result = sync.apply_overlay(source, name)
            self.assertEqual(result.decode(), (sync.PATCH / 'overlay' / name).read_text())

    def test_conflicting_change_is_rejected(self):
        source = (sync.PATCH / 'modern/ha-proxy.js').read_text()
        source = source.replace("const SID_COOKIE = 'openccu_ingress_sid';", "const SID_COOKIE = 'new_upstream_protocol';")
        with self.assertRaisesRegex(ValueError, 'patch conflict'):
            sync.apply_overlay(source.encode(), 'ha-proxy.js')

    def test_unrelated_upstream_changes_survive(self):
        source = (sync.PATCH / 'modern/ha-proxy.js').read_text().replace('// Node.js based', '// Improved Node.js based')
        result = sync.apply_overlay(source.encode(), 'ha-proxy.js')
        self.assertIn(b'// Improved Node.js based', result)

    def test_versions_preserve_snapshot_and_increment_revision(self):
        self.assertEqual(sync.app_version('3.89.8.20260826-dfd4f38', {}), '3.89.8.20260826-dfd4f38-ha1')
        self.assertEqual(sync.app_version('0.7.0', {'upstream_version': '0.7.0', 'revision': 3}), '0.7.0-ha4')
        self.assertEqual(sync.app_version('0.8.0', {'upstream_version': '0.7.0', 'revision': 3}), '0.8.0-ha1')

    def test_missing_image_architecture_fails(self):
        with patch.object(sync, 'request', side_effect=[b'{"token":"test"}', b'{"manifests":[]}']):
            with self.assertRaisesRegex(ValueError, 'architectures'):
                sync.image_digest('ghcr.io/openccu/openccu', 'test')

    def test_all_apps_are_pinned_and_login_is_opt_in(self):
        import yaml
        for slug in sync.APPS:
            directory = ROOT / 'apps' / slug
            lock = json.loads((directory / 'upstream.lock.json').read_text())
            docker = (directory / 'Dockerfile').read_text()
            config = yaml.safe_load((directory / 'config.yaml').read_text())
            self.assertIn('@' + lock['image_digest'], docker)
            self.assertTrue(config['image'].startswith('ghcr.io/sandmaennchen5/ha-repo-'))
            if slug == 'openccu-hapdrap':
                self.assertFalse(config.get('ingress', False))
                self.assertNotIn('remember_ingress_users', config['options'])
                continue
            self.assertFalse(config['options']['remember_ingress_users'])
            self.assertFalse(config['options']['remember_ingress_credentials'])
            self.assertIn(lock['original_proxy_sha256'], docker)
            self.assertIn(lock['patched_proxy_sha256'], docker)
            name = 'rootfs/app/ha-proxy.js.gtpl' if slug.endswith('proxy') else 'rootfs/bin/ha-proxy.js'
            self.assertEqual(sync.sha((directory / name).read_text().encode()), lock['patched_proxy_sha256'])


if __name__ == '__main__':
    unittest.main()
