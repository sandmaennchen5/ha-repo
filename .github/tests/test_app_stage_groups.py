from html.parser import HTMLParser
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

from jinja2 import Environment, FileSystemLoader

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))

import readme_generator
from badge_generator import get_app_stage
from utils import load_config_sections


class AppTables(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tables = {}
        self.current = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'table':
            self.current = attrs.get('id')
            self.tables[self.current] = []
        elif tag == 'tr' and self.current and 'data-slug' in attrs:
            self.tables[self.current].append(attrs['data-slug'])

    def handle_endtag(self, tag):
        if tag == 'table':
            self.current = None


class AppStageGroupTests(unittest.TestCase):
    def test_stage_uses_config_then_metadata_then_stable(self):
        for config, metadata, expected in [
            ({'stage': 'stable'}, {'stage': 'deprecated'}, 'stable'),
            ({}, {'stage': 'deprecated'}, 'deprecated'),
            ({}, {}, 'stable'),
            ({'stage': ' Deprecated '}, {}, 'deprecated'),
        ]:
            self.assertEqual(get_app_stage({'app': config, 'var': metadata}), expected)

    def test_readme_places_deprecated_after_all_other_stages(self):
        paths = [Path('apps/a-old'), Path('apps/b-experimental'),
                 Path('apps/c-old'), Path('apps/d-stable'), Path('apps/e-hidden')]
        stages = ['deprecated', 'experimental', 'deprecated', 'stable', 'deprecated']
        data = {p: {'app': {'name': p.name, 'stage': stage},
                    'var': {'hide_root_readme': p.name == 'e-hidden'}}
                for p, stage in zip(paths, stages)}
        with patch.object(readme_generator, 'get_apps', return_value=paths), \
             patch.object(readme_generator, 'load_app', side_effect=data.__getitem__), \
             patch.object(readme_generator, 'generate_app_badges', return_value=[]):
            text = readme_generator.build_root_section()
            english = readme_generator.build_root_section('Deprecated apps')
        positions = [text.index(value) for value in
                     ['b-experimental', 'd-stable', '## Veraltete Apps (deprecated)', 'a-old', 'c-old']]
        self.assertEqual(positions, sorted(positions))
        self.assertNotIn('e-hidden', text)
        self.assertIn('### [a-old]', text)
        self.assertIn('## Deprecated apps', english)

    def render_apps(self, apps):
        env = Environment(loader=FileSystemLoader(SCRIPTS / 'dashboard/templates'))
        _, config = load_config_sections()
        return env.get_template('apps.html').render(
            config=config, apps=apps, site=config['site'], theme=config['theme'],
            base_url=config['site']['base_url'], asset_path='assets')

    def test_dashboard_separate_tables_preserve_order_and_shared_filter(self):
        apps = [{'slug': slug, 'name': slug, 'stage': stage} for slug, stage in
                [('a-old', 'deprecated'), ('b-test', 'experimental'),
                 ('c-old', 'deprecated'), ('d-stable', 'stable')]]
        html = self.render_apps(apps)
        tables = AppTables()
        tables.feed(html)
        self.assertEqual(tables.tables['appsTable'], ['b-test', 'd-stable'])
        self.assertEqual(tables.tables['deprecatedAppsTable'], ['a-old', 'c-old'])
        self.assertLess(html.index('id="appsTable"'), html.index('id="deprecatedAppsTable"'))
        self.assertIn('Veraltete Apps (deprecated)', html)
        self.assertIn('".apps-table tbody tr"', html)
        self.assertEqual(html.count('class="favorite-btn"'), 4)

    def test_no_empty_deprecated_section(self):
        html = self.render_apps([{'slug': 'current', 'name': 'current', 'stage': 'stable'}])
        self.assertNotIn('id="deprecatedAppsTable"', html)
        self.assertNotIn('<h2>Veraltete Apps (deprecated)</h2>', html)


if __name__ == '__main__':
    unittest.main()
