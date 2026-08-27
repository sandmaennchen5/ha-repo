#!/usr/bin/env python3
"""Stage OpenCCU updates from upstream; publish images BEFORE committing config versions.

The fork is NOT an update feed. Its reviewed overlay is vendored at a fixed commit.
Patch conflicts, unavailable images and source/image mismatches fail closed.
"""
from __future__ import annotations

import argparse
import datetime as dt
import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import urllib.parse
import urllib.error
import urllib.request

import yaml

ROOT = Path(__file__).resolve().parents[2]
PATCH = ROOT / '.github/openccu'
PATCH_COMMIT = '4a84f7aa7c69ac93685080a02f40832fc63fcbfa'
APPS = {
    'openccu': 'home-assistant-addon',
    'openccu-dev': 'home-assistant-addon-dev',
    'openccu-proxy': 'home-assistant-addon-proxy',
    'openccu-hapdrap': 'home-assistant-addon-hapdrap',
}
PROXY_SOURCE = 'buildroot-external/overlay/base-openccu_oci/bin/ha-proxy.js'
OPTIONS = {'remember_ingress_users': False, 'remember_ingress_credentials': False,
           'ingress_keepalive_interval': 250}
SCHEMA = {'remember_ingress_users': 'bool', 'remember_ingress_credentials': 'bool',
          'ingress_keepalive_interval': 'int(1,599)'}


class IndentedSafeDumper(yaml.SafeDumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


def dump_yaml(value) -> bytes:
    return yaml.dump(value, Dumper=IndentedSafeDumper, allow_unicode=True, sort_keys=False).encode()


def normalize_config(config):
    config = dict(config)
    # Explicit HA defaults are discouraged by the app linter. Removing only
    # exact default values preserves the upstream runtime behavior.
    for key, default in {'ingress': False, 'apparmor': True, 'boot': 'auto'}.items():
        if key in config and type(config[key]) is type(default) and config[key] == default:
            del config[key]
    return config


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def request(url: str, headers=None) -> bytes:
    headers = dict(headers or {})
    headers['User-Agent'] = 'ha-repo-openccu-sync'
    if url.startswith('https://api.github.com/') and os.getenv('GITHUB_TOKEN'):
        headers['Authorization'] = 'Bearer ' + os.environ['GITHUB_TOKEN']
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60) as response:
        return response.read()


def github(path: str):
    return json.loads(request('https://api.github.com/repos/OpenCCU/OpenCCU/' + path))


def raw(ref: str, path: str) -> bytes:
    return request(f'https://raw.githubusercontent.com/OpenCCU/OpenCCU/{ref}/{path}')


def image_digest(image: str, version: str) -> str:
    if not re.fullmatch(r'ghcr\.io/openccu/[a-z0-9-]+', image):
        raise ValueError('Unexpected upstream image: ' + image)
    repo = image.removeprefix('ghcr.io/')
    query = urllib.parse.urlencode({'service': 'ghcr.io', 'scope': f'repository:{repo}:pull'})
    token = json.loads(request('https://ghcr.io/token?' + query))['token']
    data = request(f'https://ghcr.io/v2/{repo}/manifests/{urllib.parse.quote(version, safe="")}', {
        'Authorization': 'Bearer ' + token,
        'Accept': 'application/vnd.oci.image.index.v1+json, application/vnd.docker.distribution.manifest.list.v2+json',
    })
    manifest = json.loads(data)
    platforms = {(m.get('platform', {}).get('os'), m.get('platform', {}).get('architecture'))
                 for m in manifest.get('manifests', [])}
    if not {('linux', 'amd64'), ('linux', 'arm64')} <= platforms:
        raise ValueError(f'{image}:{version}: both supported architectures must exist')
    return 'sha256:' + sha(data)


def apply_overlay(original: bytes, name: str) -> bytes:
    """Apply only exact-context changes, preserving unrelated upstream changes.

    Stable backport also carries prerequisite upstream SID-cookie changes. Both
    baselines are explicit and reviewed. No fuzzy patch or blind replacement.
    """
    target = (PATCH / 'overlay' / name).read_text(encoding='utf-8')
    for baseline in ['modern', 'stable']:
        source = PATCH / baseline / name
        if not source.exists():
            continue
        delta = ''.join(difflib.unified_diff(
            source.read_text(encoding='utf-8').splitlines(keepends=True),
            target.splitlines(keepends=True), fromfile='a/proxy.js', tofile='b/proxy.js'))
        with tempfile.TemporaryDirectory(prefix='openccu-patch-') as directory:
            file = Path(directory) / 'proxy.js'
            file.write_bytes(original)
            result = subprocess.run(['git', 'apply', '--check', '-'], input=delta.encode(),
                                    cwd=directory, capture_output=True)
            if result.returncode:
                continue
            subprocess.run(['git', 'apply', '-'], input=delta.encode(), cwd=directory,
                           capture_output=True, check=True)
            patched = file.read_bytes().replace(b'\r\n', b'\n')
            # Templates are rendered by the official entrypoint. Validate JS with
            # only the known URL placeholders replaced, without executing it.
            check = patched.decode().replace('{{ printf "%q" (index . "webui-url") }}', '"http://openccu"')
            check = check.replace('{{ index . "webui-url" }}', 'http://openccu')
            subprocess.run(['node', '--check'], input=check.encode(), capture_output=True, check=True)
            return patched
    raise ValueError(f'OpenCCU patch conflict in {name}; review upstream before publishing')


def app_version(upstream: str, old: dict) -> str:
    revision = int(old.get('revision', 0)) + 1 if old.get('upstream_version') == upstream else 1
    # HA accepts suffixes; keep the original snapshot identity intact.
    return f'{upstream}-ha{revision}'


def generate(slug: str, folder: str, metadata_ref: str) -> dict[str, bytes]:
    config_raw = raw(metadata_ref, folder + '/config.yaml')
    config = yaml.safe_load(config_raw)
    upstream = str(config['version'])
    image = config['image']
    if config['arch'] != ['aarch64', 'amd64']:
        raise ValueError(f'{slug}: upstream architectures changed; review required')
    digest = image_digest(image, upstream)
    files = {}
    original = patched = b''
    source_ref = metadata_ref
    if slug in ('openccu', 'openccu-dev'):
        source_ref = upstream if slug == 'openccu' else upstream.rsplit('-', 1)[-1]
        source_ref = github('commits/' + urllib.parse.quote(source_ref, safe=''))['sha']
        original = raw(source_ref, PROXY_SOURCE)
        patched = apply_overlay(original, 'ha-proxy.js')
        destination = '/bin/ha-proxy.js'
    elif slug == 'openccu-proxy':
        original = raw(metadata_ref, folder + '/ha-proxy.js.gtpl')
        patched = apply_overlay(original, 'ha-proxy.js.gtpl')
        destination = '/app/ha-proxy.js.gtpl'
    if patched:
        files['rootfs' + destination] = patched
        config.setdefault('options', {}).update(OPTIONS)
        config.setdefault('schema', {}).update(SCHEMA)
    # Preserve all hardware access, ports, mounts and helper settings from upstream.
    config['name'] += ' (HA Repo)'
    config['image'] = 'ghcr.io/sandmaennchen5/ha-repo-' + slug
    config['slug'] = slug
    config['url'] = 'https://github.com/sandmaennchen5/ha-repo/tree/main/apps/' + slug
    config['stage'] = 'experimental'
    # Pull translations/licensing from the original; local option labels are added below.
    for item in github(f'contents/{folder}?ref={metadata_ref}'):
        if item['type'] == 'file' and item['name'] == 'apparmor.txt':
            files[item['name']] = raw(metadata_ref, folder + '/' + item['name'])
    files['LICENSE.upstream'] = raw(metadata_ref, 'LICENSE')
    for language in ['en', 'de']:
        translations = {'configuration': {}}
        try:
            translations = yaml.safe_load(raw(metadata_ref, folder + f'/translations/{language}.yaml')) or translations
        except urllib.error.HTTPError as error:
            if error.code != 404:
                raise
        if patched:
            for key, label in {
                'remember_ingress_users': ('Ingress-Sitzung merken', 'Remember Ingress session'),
                'remember_ingress_credentials': ('Zugangsdaten verschlüsselt speichern', 'Store encrypted credentials'),
                'ingress_keepalive_interval': ('Sitzung erneuern (Sekunden)', 'Session keep-alive interval (seconds)'),
            }.items():
                translations.setdefault('configuration', {})[key] = {'name': label[language == 'en']}
        files[f'translations/{language}.yaml'] = dump_yaml(translations)
    lock = {
        'upstream_version': upstream, 'image': image, 'image_digest': digest,
        'metadata_commit': metadata_ref, 'source_commit': source_ref,
        'patch_commit': PATCH_COMMIT if patched else None,
        'original_proxy_sha256': sha(original) if original else None,
        'patched_proxy_sha256': sha(patched) if patched else None,
        'config_sha256': sha(config_raw),
    }
    old_file = ROOT / 'apps' / slug / 'upstream.lock.json'
    old = json.loads(old_file.read_text()) if old_file.exists() else {}
    # Ignore unrelated commits; metadata must not cause daily version bumps.
    meaningful = [k for k in lock if k not in ('metadata_commit', 'source_commit')]
    if old and all(old.get(k) == lock[k] for k in meaningful):
        return {}
    version = app_version(upstream, old)
    lock['revision'] = int(version.rsplit('-ha', 1)[1])
    config['version'] = version
    files['config.yaml'] = dump_yaml(normalize_config(config))
    files['upstream.lock.json'] = (json.dumps(lock, indent=2) + '\n').encode()
    # No dependency on a floating fork or ARG override: original image is immutable.
    docker = f'ARG UPSTREAM_VERSION={upstream}\nFROM {image}:{upstream}@{digest}\n'
    if patched:
        docker += f'RUN echo "{sha(original)}  {destination}" | sha256sum -c -\n'
        mode = '644' if destination.endswith('.gtpl') else '755'
        docker += f'COPY --chmod={mode} rootfs{destination} {destination}\n'
        docker += f'RUN echo "{sha(patched)}  {destination}" | sha256sum -c -\n'
    docker += 'LABEL org.opencontainers.image.source="https://github.com/sandmaennchen5/ha-repo"\n'
    files['Dockerfile'] = docker.encode()
    var = {'hidden': False, 'icon': '🏠', 'stage': 'experimental',
           'version_strategy': 'upstream_revision', 'upstream_strategy': 'openccu_overlay',
           'upstream_version': upstream, 'upstream_repo': 'https://github.com/OpenCCU/OpenCCU',
           'upstream_commit': digest, 'autoupdater': True,
           'updated': dt.date.today().isoformat(), 'source': 'github.com/OpenCCU/OpenCCU'}
    files['.var.yaml'] = dump_yaml(var)
    changelog = ROOT / 'apps' / slug / 'CHANGELOG.md'
    history = changelog.read_text(encoding='utf-8').removeprefix('# Changelog\n').lstrip() if changelog.exists() else ''
    files['CHANGELOG.md'] = (f'# Changelog\n\n## {version}\n\n- Original: `{image}:{upstream}`.\n'
                            '- Pinned image and checked overlay; original runtime retained.\n\n' + history).encode()
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--export', action='store_true', help='print generated text files as JSON, do not write')
    parser.add_argument('--output', type=Path, default=ROOT, help='staging repository root')
    args = parser.parse_args()
    ref = github('commits/master')['sha']
    # Generate and validate ALL candidates before writing anything.
    changes = {}
    for slug, folder in APPS.items():
        for name, data in generate(slug, folder, ref).items():
            changes[f'apps/{slug}/{name}'] = data.decode('utf-8')
    if args.export:
        print(json.dumps(changes, ensure_ascii=True))
        return
    for name, content in changes.items():
        file = args.output / name
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(content, encoding='utf-8', newline='\n')
    print(f'Generated {len(changes)} files; publish images before committing these versions.')


if __name__ == '__main__':
    main()
