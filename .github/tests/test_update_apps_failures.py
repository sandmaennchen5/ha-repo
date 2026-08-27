import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('update_apps_under_test', ROOT / '.github/scripts/update_apps.py')
updater = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = updater
spec.loader.exec_module(updater)


class UpdateFailureTests(unittest.TestCase):
    def test_http_error_has_endpoint_and_rate_limit_without_secrets(self):
        error = HTTPError('https://user:password@hub.docker.com/v2/repositories/portainer/tags?token=secret',
                          403, 'Forbidden', {'X-RateLimit-Remaining': '0'}, None)
        message = updater.describe_error(error)
        self.assertIn('HTTP 403 at https://hub.docker.com/v2/repositories/portainer/tags', message)
        self.assertIn('X-RateLimit-Remaining=0', message)
        for secret in ('password', 'user:', 'token', 'secret'):
            self.assertNotIn(secret, message)

    def test_partial_writes_are_restored_byte_for_byte(self):
        with tempfile.TemporaryDirectory() as directory:
            app = Path(directory)
            (app / 'config.yaml').write_bytes(b'version: old\r\n')
            def failing_apply(*args):
                (app / 'config.yaml').write_text('version: broken')
                (app / 'CHANGELOG.md').write_text('partial')
                raise ValueError('bad update')
            with patch.object(updater, 'apply', side_effect=failing_apply):
                with self.assertRaises(ValueError):
                    updater.process_app(app, 'docker', ('test', 'test'), preview_only=False, bump=False)
            self.assertEqual((app / 'config.yaml').read_bytes(), b'version: old\r\n')
            self.assertFalse((app / 'CHANGELOG.md').exists())

    def test_failed_bump_rolls_back_the_app_update(self):
        with tempfile.TemporaryDirectory() as directory:
            app = Path(directory)
            (app / 'config.yaml').write_text('old')
            with patch.object(updater, 'apply', side_effect=lambda *args: (app / 'config.yaml').write_text('new')):
                with patch.object(updater, 'bump_app_revision', side_effect=ValueError('bad bump')):
                    with self.assertRaises(ValueError):
                        updater.process_app(app, 'docker', ('test', 'test'), preview_only=False, bump=True)
            self.assertEqual((app / 'config.yaml').read_text(), 'old')

    def test_all_apps_processed_and_failure_outputs_preserved(self):
        for continued in (False, True):
            with self.subTest(continued=continued), tempfile.TemporaryDirectory() as directory:
                base = Path(directory)
                output, summary = base / 'output', base / 'summary'
                apps = [(base / name, 'docker', ('test', name)) for name in ('first', 'bad', 'last')]
                visited = []
                def process(path, *args, **kwargs):
                    visited.append(path.name)
                    if path.name == 'bad':
                        raise HTTPError('https://hub.docker.com/v2/bad', 403, 'Forbidden', {}, None)
                argv = ['update_apps.py'] + (['--continue-on-error'] if continued else [])
                with patch.object(sys, 'argv', argv), patch.dict(os.environ, {'GITHUB_OUTPUT':str(output), 'GITHUB_STEP_SUMMARY':str(summary)}):
                    with patch.object(updater, 'discover', return_value=(apps, [])), patch.object(updater, 'process_app', side_effect=process):
                        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                            self.assertEqual(updater.main(), 0 if continued else 1)
                self.assertEqual(visited, ['first', 'bad', 'last'])
                self.assertEqual(json.loads(output.read_text().split('=', 1)[1]), ['bad'])
                self.assertIn('bad: HTTP 403 at https://hub.docker.com/v2/bad', summary.read_text())

    def test_workflow_defers_error_status_until_after_builds(self):
        import yaml
        jobs = yaml.safe_load((ROOT / '.github/workflows/update-apps.yaml').read_text())['jobs']
        steps = jobs['update']['steps']
        discovery = next(step for step in steps if step.get('id') == 'discover')
        self.assertIn('--continue-on-error', discovery['run'])
        matrix = next(step for step in steps if step.get('id') == 'build_plan')
        self.assertIn('$apps - $failed', matrix['run'])
        report = jobs['report-update-errors']
        self.assertEqual(report['needs'], ['update', 'build'])
        self.assertIn('always()', report['if'])
        self.assertIn('exit 1', report['steps'][0]['run'])


if __name__ == '__main__':
    unittest.main()
