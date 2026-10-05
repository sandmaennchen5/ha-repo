"""Emit severity-aware annotations; warnings never fail the lint job."""
import json
from pathlib import Path
import sys


def escape(value, property_value=False):
    value = str(value).replace('%', '%25').replace('\r', '%0D').replace('\n', '%0A')
    return value.replace(':', '%3A').replace(',', '%2C') if property_value else value


def report(findings):
    if not isinstance(findings, list):
        raise ValueError('Expected hadolint JSON list')
    failed = False
    for item in findings:
        level = item['level']
        if level not in ('error', 'warning', 'info', 'style', 'ignore'):
            raise ValueError(f'Unknown hadolint severity: {level}')
        severity = 'error' if level == 'error' else 'warning'
        failed |= severity == 'error'
        print(f"::{severity} file={escape(item['file'], True)},line={max(1, int(item['line']))}::"
              f"{escape(item['code'])} ({level}): {escape(item['message'])}")
    return int(failed)


if __name__ == '__main__':
    sys.exit(report(json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))))
