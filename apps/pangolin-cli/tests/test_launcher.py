"""Exercise the real launcher with mocked bashio and CLI (no tunnel needed)."""
import os
from pathlib import Path
import shlex
import subprocess
import unittest

import yaml

APP = Path(__file__).resolve().parents[1]
RUN = APP / 'rootfs/etc/s6-overlay/s6-rc.d/pangolin-cli/run'


class LauncherTests(unittest.TestCase):
    def launch(self, values, role=None):
        config = {'endpoint': 'https://example.com', 'extras.log_level': 'info', **values}
        entries = ' '.join(f'[{shlex.quote(k)}]={shlex.quote(str(v))}' for k, v in config.items())
        prelude = '''declare -A config=(ENTRIES)
bashio::config() { printf '%s' "${config[$1]-}"; }
bashio::config.has_value() { [[ -n "${config[$1]-}" ]]; }
bashio::log.fatal() { printf 'FATAL:%s\n' "$*" >&2; }
bashio::log.info() { :; }
pangolin-cli() {
  printf 'ARG:%s\n' "$@"
  env | sort
}
'''.replace('ENTRIES', entries)
        # A function cannot replace an exec target; remove only exec for the mock.
        select_role = 'set -- site\n' if role == 'site' else 'set --\n'
        script = prelude + select_role + RUN.read_text(encoding='utf-8').replace(
            'exec pangolin-cli ', 'pangolin-cli ').replace(
            'exec sleep infinity', "printf 'INACTIVE\\n'; exit 0")
        env = {k: v for k, v in os.environ.items() if not k.startswith(('SITE_', 'NEWT_', 'CLIENT_'))}
        bash = os.environ.get('BASH_TEST_EXECUTABLE', 'bash')
        return subprocess.run([bash, '-c', script], env=env, text=True, capture_output=True)

    def test_legacy_client_and_literal_arguments(self):
        result = self.launch({'client_id': 'client-test', 'client_secret': 'secret-test',
                              'extras.additional_args': '--example * $(false)'})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('ARG:--attach\n', result.stdout)
        self.assertIn('ARG:*\nARG:$(false)\n', result.stdout)
        self.assertIn('CLIENT_ID=client-test\n', result.stdout)
        self.assertNotIn('SITE_ID=', result.stdout)

    def test_site_credentials_false_and_spaces(self):
        result = self.launch({'mode': 'site', 'site_id': 'site-test', 'site_secret': 'secret-test',
                              'site.metrics': 'false', 'site.name': 'My home site',
                              'site.tls_client_ca': '/config/a.pem,/config/b.pem',
                              'site.prefer_endpoint': 'https://preferred.example.com',
                              'extras.log_level': 'trace'})
        self.assertEqual(result.returncode, 0, result.stderr)
        for value in ['ARG:up\nARG:site\n', 'SITE_ID=site-test\n',
                      'SITE_METRICS_PROMETHEUS_ENABLED=false\n', 'SITE_NAME=My home site\n',
                      'TLS_CLIENT_CAS=/config/a.pem,/config/b.pem\n',
                      'CONFIG_FILE=/data/pangolin-site.json\n', 'LOG_LEVEL=DEBUG\n',
                      'ARG:--prefer-endpoint\nARG:https://preferred.example.com\n']:
            self.assertIn(value, result.stdout)
        self.assertNotIn('ARG:--attach', result.stdout)
        self.assertNotIn('CLIENT_ID=', result.stdout)

    def test_provisioning_without_credentials(self):
        result = self.launch({'mode': 'site', 'site.provisioning_key': 'dummy-key'})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('SITE_PROVISIONING_KEY=dummy-key\n', result.stdout)

    def test_existing_config_without_credentials(self):
        result = self.launch({'mode': 'site', 'site.config_file': '/dev/null'})
        # /dev/null is not a regular file and must not bypass validation.
        self.assertNotEqual(result.returncode, 0)
        result = self.launch({'mode': 'site', 'site.config_file': '/etc/hosts'})
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_missing_and_partial_credentials(self):
        for values in [{'client_id': 'dummy'}, {'mode': 'site'},
                       {'mode': 'site', 'site_id': 'dummy'},
                       {'mode': 'site', 'site_secret': 'dummy'}, {'mode': 'invalid'}]:
            with self.subTest(values=values):
                result = self.launch(values)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('FATAL:', result.stderr)
                self.assertNotIn('ARG:', result.stdout)

    def test_every_site_schema_option_is_forwarded(self):
        schema = yaml.safe_load((APP / 'config.yaml').read_text(encoding='utf-8'))['schema']['site']
        for key, kind in schema.items():
            if key == 'prefer_endpoint':
                continue
            value = 'false' if kind == 'bool?' else '1234' if kind.startswith('int') else 'test-value'
            result = self.launch({'mode': 'site', 'site_id': 'dummy', 'site_secret': 'dummy',
                                  f'site.{key}': value})
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(f'={value}\n', result.stdout, key)

    def test_dual_runs_both_roles_with_isolated_options(self):
        values = {'mode': 'dual', 'client_id': 'client-test', 'client_secret': 'client-secret',
                  'site_id': 'site-test', 'site_secret': 'site-secret',
                  'extras.additional_args': '--legacy-client',
                  'extras.client_additional_args': '--client-only',
                  'extras.site_additional_args': '--site-only', 'site.metrics': 'true'}
        client = self.launch(values)
        site = self.launch(values, role='site')
        self.assertEqual(client.returncode, 0, client.stderr)
        self.assertEqual(site.returncode, 0, site.stderr)
        self.assertIn('ARG:--attach\n', client.stdout)
        self.assertIn('ARG:--interface-name\nARG:pangolin-client\n', client.stdout)
        self.assertIn('ARG:--legacy-client\nARG:--client-only\n', client.stdout)
        self.assertNotIn('ARG:--site-only', client.stdout)
        self.assertNotIn('SITE_ID=', client.stdout)
        self.assertIn('ARG:up\nARG:site\n', site.stdout)
        self.assertIn('ARG:--site-only\n', site.stdout)
        self.assertNotIn('ARG:--legacy-client', site.stdout)
        self.assertNotIn('ARG:--client-only', site.stdout)
        self.assertNotIn('CLIENT_ID=', site.stdout)
        self.assertIn('INTERFACE=pangolin-site\n', site.stdout)
        self.assertIn('INTERFACE_MAIN=pangolin-main\n', site.stdout)

    def test_dual_explicit_interfaces_and_client_http(self):
        values = {'mode': 'dual', 'client_id': 'dummy', 'client_secret': 'dummy',
                  'site_id': 'dummy', 'site_secret': 'dummy',
                  'client.interface_name': 'vpn-client', 'client.http_addr': '127.0.0.1:2113',
                  'site.interface': 'vpn-site', 'site.interface_main': 'vpn-main'}
        client = self.launch(values)
        site = self.launch(values, role='site')
        self.assertIn('ARG:--interface-name\nARG:vpn-client\n', client.stdout)
        self.assertIn('ARG:--http-addr\nARG:127.0.0.1:2113\n', client.stdout)
        self.assertIn('INTERFACE=vpn-site\n', site.stdout)
        self.assertIn('INTERFACE_MAIN=vpn-main\n', site.stdout)

    def test_secondary_service_inactive_in_single_modes(self):
        for mode in ['client', 'site']:
            result = self.launch({'mode': mode}, role='site')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, 'INACTIVE\n')

    def test_dual_requires_credentials_for_each_active_role(self):
        client = self.launch({'mode': 'dual', 'site_id': 'dummy', 'site_secret': 'dummy'})
        site = self.launch({'mode': 'dual', 'client_id': 'dummy', 'client_secret': 'dummy'}, role='site')
        for result in [client, site]:
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('FATAL:', result.stderr)

    def test_both_services_registered_for_supervision(self):
        services = APP / 'rootfs/etc/s6-overlay/s6-rc.d'
        for name in ['pangolin-cli', 'pangolin-site']:
            self.assertEqual((services / name / 'type').read_text().strip(), 'longrun')
            self.assertTrue((services / 'user/contents.d' / name).is_file())
        self.assertIn('/pangolin-cli/run site', (services / 'pangolin-site/run').read_text())

    def test_health_requires_each_active_cli(self):
        health = (APP / 'rootfs/usr/local/bin/pangolin-healthcheck').read_text()
        # Mock only the operating-system boundary; execute actual health logic.
        health = health.replace('read -r name < "/proc/${pid}/comm"',
                                'name="${names[$service]}"')
        for mode, client_up, site_up, site_name, expected in [
            ('client', 'true', 'false', 'sleep', 0),
            ('site', 'true', 'false', 'sleep', 0),
            ('dual', 'true', 'true', 'pangolin-cli', 0),
            ('dual', 'true', 'false', 'pangolin-cli', 1),
            ('dual', 'false', 'true', 'pangolin-cli', 1),
            ('dual', 'true', 'true', 'sleep', 1),
            ('dual', 'true', 'true', 'bash', 1),
        ]:
            mock = f'''declare -A names=([pangolin-cli]=pangolin-cli [pangolin-site]={site_name})
bashio::config.has_value() {{ return 0; }}
bashio::config() {{ printf '%s' {mode}; }}
s6-svstat() {{
  if [[ "$3" == */pangolin-cli ]]; then printf '{client_up} 123\\n';
  else printf '{site_up} 456\\n'; fi
}}
kill() {{ return 0; }}
'''
            result = subprocess.run([os.environ.get('BASH_TEST_EXECUTABLE', 'bash'), '-c', mock + health],
                                    text=True, capture_output=True)
            self.assertEqual(result.returncode, expected, (mode, client_up, site_up, site_name, result.stderr))


if __name__ == '__main__':
    unittest.main()
