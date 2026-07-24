#!/usr/bin/env python3
"""Update Home Assistant apps from GitHub releases or Docker Hub tags."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from packaging.version import InvalidVersion, Version


ROOT = Path(__file__).resolve().parents[2]
APPS = ROOT / "apps"
USER_AGENT = "ha-app-autoupdater/1.0"
GITHUB_RE = re.compile(r"^(?:https?://)?github\.com/([^/]+)/([^/#]+?)(?:\.git)?/?$")
DOCKER_RE = re.compile(r"^(?:https?://)?(?:docker\.io/)?([^/]+)/([^/:@]+)(?::[^@]+)?$")


@dataclass(frozen=True)
class Update:
    version: str
    commit: str
    updated: str
    source: str
    notes: str
    kind: str


def request_json(url: str, token: str = "") -> tuple[Any, dict[str, str]]:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": USER_AGENT}
    if token:
        headers["Authorization"] = f"Bearer {token}"
        headers["X-GitHub-Api-Version"] = "2022-11-28"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response), dict(response.headers.items())


def source_kind(value: str) -> tuple[str, tuple[str, str]] | None:
    value = value.strip()
    match = GITHUB_RE.match(value)
    if match:
        return "github", (match.group(1), match.group(2))
    match = DOCKER_RE.match(value)
    if match:
        namespace, repository = match.groups()
        if namespace == "library" or value.startswith("docker.io/"):
            return "docker", (namespace, repository)
    return None


def clean_version(tag: str) -> str:
    return tag[1:] if re.match(r"^v\d", tag, re.IGNORECASE) else tag


def iso_date(value: str) -> str:
    return value[:10] if value else dt.date.today().isoformat()


def github_update(owner: str, repository: str, configured_source: str) -> Update:
    token = os.getenv("GITHUB_TOKEN", "")
    api = f"https://api.github.com/repos/{owner}/{repository}"
    release, _ = request_json(f"{api}/releases/latest", token)
    tag = release["tag_name"]
    commit = ""
    try:
        ref, _ = request_json(f"{api}/git/ref/tags/{urllib.parse.quote(tag, safe='')}", token)
        obj = ref["object"]
        if obj.get("type") == "tag":
            obj, _ = request_json(obj["url"], token)
            obj = obj["object"]
        commit = obj.get("sha", "")
    except (KeyError, urllib.error.HTTPError):
        commit = release.get("target_commitish", "")
    source = f"github.com/{owner}/{repository}"
    return Update(
        version=clean_version(tag),
        commit=commit,
        updated=iso_date(release.get("published_at") or release.get("created_at", "")),
        source=source if configured_source else source,
        notes=(release.get("body") or "Keine Release Notes vorhanden.").strip(),
        kind="github",
    )


def semantic(tag: str) -> Version | None:
    try:
        version = Version(clean_version(tag))
        return version if not version.is_prerelease and not version.is_devrelease else None
    except InvalidVersion:
        return None


def docker_update(namespace: str, repository: str) -> Update:
    base = f"https://hub.docker.com/v2/repositories/{namespace}/{repository}/tags"
    url = f"{base}?page_size=100&ordering=last_updated"
    tags: list[dict[str, Any]] = []
    while url:
        page, _ = request_json(url)
        tags.extend(page.get("results", []))
        url = page.get("next")

    latest = next((tag for tag in tags if tag.get("name") == "latest"), None)
    semver_tags = [(semantic(tag.get("name", "")), tag) for tag in tags]
    semver_tags = [(version, tag) for version, tag in semver_tags if version is not None]
    if not semver_tags:
        raise RuntimeError(f"docker.io/{namespace}/{repository}: no semantic version tag found")

    same_digest = []
    if latest and latest.get("digest"):
        same_digest = [item for item in semver_tags if item[1].get("digest") == latest["digest"]]
    version_obj, selected = max(same_digest or semver_tags, key=lambda item: item[0])
    digest = selected.get("digest") or (latest or {}).get("digest", "")
    tag = selected["name"]
    source = f"docker.io/{namespace}/{repository}"
    notes = (
        f"- Docker Hub image: `{source}:{tag}`\n"
        f"- Digest: `{digest or 'nicht verfügbar'}`\n"
        f"- Aktualisiert auf Docker Hub: {iso_date(selected.get('last_updated', ''))}"
    )
    return Update(
        version=clean_version(tag),
        commit=digest,
        updated=iso_date(selected.get("last_updated", "")),
        source=source,
        notes=notes,
        kind="docker",
    )


def replace_scalar(text: str, key: str, value: str) -> str:
    pattern = re.compile(rf"^(?P<indent>\s*){re.escape(key)}\s*:\s*.*$", re.MULTILINE)
    replacement = lambda match: f'{match.group("indent")}{key}: {json.dumps(value, ensure_ascii=False)}'
    if pattern.search(text):
        return pattern.sub(replacement, text, count=1)
    suffix = "" if text.endswith("\n") else "\n"
    return f"{text}{suffix}{key}: {json.dumps(value, ensure_ascii=False)}\n"


def update_changelog(path: Path, update: Update) -> None:
    original = path.read_text(encoding="utf-8") if path.exists() else "# Changelog\n"
    heading = f"## [{update.version}]"
    if heading in original:
        if update.kind == "manual":
            manual_entry = f"### Manuelles Update ({update.updated})\n\n{update.notes}\n"
            if manual_entry in original:
                return
            heading_pattern = re.compile(
                rf"^(## \[{re.escape(update.version)}\][^\n]*\n)",
                re.MULTILINE,
            )
            result = heading_pattern.sub(
                lambda match: f"{match.group(1)}\n{manual_entry}\n",
                original,
                count=1,
            )
            path.write_text(result, encoding="utf-8", newline="\n")
        return
    entry = f"## [{update.version}] - {update.updated}\n\n"
    if update.kind == "docker":
        entry += f"### Docker Hub\n\n{update.notes}\n"
    elif update.kind == "github":
        entry += f"### Upstream Release Notes\n\n{update.notes}\n"
    else:
        entry += f"### Manuelles Update\n\n{update.notes}\n"
    if update.source:
        source_url = update.source if update.source.startswith(("http://", "https://")) else f"https://{update.source}"
        entry += f"\nWeitere Informationen: {source_url}"
        if update.kind == "github":
            entry += "/releases/latest"
    entry += "\n\n---\n"
    header = re.match(r"(?s)^(# .+?\n)(?:\n)?", original)
    if header:
        result = original[: header.end()] + "\n" + entry + "\n" + original[header.end() :].lstrip("\n")
    else:
        result = "# Changelog\n\n" + entry + "\n" + original
    path.write_text(result, encoding="utf-8", newline="\n")


def load_app(path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    config = yaml.safe_load((path / "config.yaml").read_text(encoding="utf-8"))
    var = yaml.safe_load((path / ".var.yaml").read_text(encoding="utf-8"))
    if not isinstance(config, dict) or not isinstance(var, dict):
        raise ValueError(f"{path.name}: YAML root must be a mapping")
    return config, var


def discover(selected: str, scheduled: bool) -> tuple[list[tuple[Path, str, tuple[str, str]]], list[str]]:
    candidates = [APPS / selected] if selected else sorted(path for path in APPS.iterdir() if path.is_dir())
    found, messages = [], []
    if selected and not candidates[0].is_dir():
        raise ValueError(f"Unknown app: {selected}")
    for path in candidates:
        required = [path / "config.yaml", path / ".var.yaml"]
        if not all(item.is_file() for item in required):
            messages.append(f"SKIP {path.name}: config.yaml or .var.yaml missing")
            continue
        _, var = load_app(path)
        raw_source = str(var.get("upstream_repo") or var.get("source") or "").strip()
        parsed = source_kind(raw_source) if raw_source else None
        if not parsed:
            messages.append(f"SKIP {path.name}: no supported upstream_repo/source")
            continue
        if scheduled and var.get("autoupdater") is not True:
            messages.append(f"SKIP {path.name}: autoupdater is not true")
            continue
        kind, identity = parsed
        messages.append(f"AUTO {path.name}: {kind} ({raw_source})")
        found.append((path, kind, identity))
    return found, messages


def apply(path: Path, kind: str, identity: tuple[str, str]) -> bool:
    config, var = load_app(path)
    raw_source = str(var.get("upstream_repo") or var.get("source") or "")
    update = github_update(*identity, raw_source) if kind == "github" else docker_update(*identity)
    if str(config.get("version", "")) == update.version and str(var.get("upstream_commit", "")) == update.commit:
        print(f"UNCHANGED {path.name}: {update.version}")
        return False
    config_path, var_path = path / "config.yaml", path / ".var.yaml"
    config_text = replace_scalar(config_path.read_text(encoding="utf-8"), "version", update.version)
    var_text = var_path.read_text(encoding="utf-8")
    for key, value in (
        ("upstream_version", update.version),
        ("upstream_commit", update.commit),
        ("updated", update.updated),
        ("source", update.source),
    ):
        var_text = replace_scalar(var_text, key, value)
    yaml.safe_load(config_text)
    yaml.safe_load(var_text)
    config_path.write_text(config_text, encoding="utf-8", newline="\n")
    var_path.write_text(var_text, encoding="utf-8", newline="\n")
    update_changelog(path / "CHANGELOG.md", update)
    print(f"UPDATED {path.name}: {config.get('version', '')} -> {update.version}")
    return True


def preview(path: Path, kind: str, identity: tuple[str, str]) -> None:
    """Fetch and display an update without changing repository files."""
    config, var = load_app(path)
    raw_source = str(var.get("upstream_repo") or var.get("source") or "")
    update = github_update(*identity, raw_source) if kind == "github" else docker_update(*identity)
    body = (
        f"## Update-Vorschau: `{path.name}`\n\n"
        "| Feld | Aktuell | Ermittelt |\n"
        "|---|---|---|\n"
        f"| Version | `{config.get('version', '')}` | `{update.version}` |\n"
        f"| Upstream-Version | `{var.get('upstream_version', '')}` | `{update.version}` |\n"
        f"| Commit/Digest | `{var.get('upstream_commit', '')}` | `{update.commit}` |\n"
        f"| Aktualisiert | `{var.get('updated', '')}` | `{update.updated}` |\n"
        f"| Quelle | `{var.get('source', '')}` | `{update.source}` |\n"
        f"| Typ |  | `{update.kind}` |\n"
    )
    print(body)
    if summary := os.getenv("GITHUB_STEP_SUMMARY"):
        with open(summary, "a", encoding="utf-8") as handle:
            handle.write(body)


def write_summary(messages: list[str], count: int, scheduled: bool) -> None:
    title = "Automatisch verarbeitete Apps" if scheduled else "Ausgewählte Apps"
    body = f"## {title}\n\n```text\n" + "\n".join(messages) + "\n```\n\n"
    body += f"{count} App(s) werden {'automatisch ' if scheduled else ''}verarbeitet.\n"
    print(body)
    if summary := os.getenv("GITHUB_STEP_SUMMARY"):
        with open(summary, "a", encoding="utf-8") as handle:
            handle.write(body)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--app", default="", help="single app slug; empty selects all")
    parser.add_argument("--scheduled", action="store_true", help="only select autoupdater: true")
    parser.add_argument("--list", action="store_true", help="discover only; do not update")
    parser.add_argument("--preview", action="store_true", help="fetch and display values without changing files")
    args = parser.parse_args()
    try:
        apps, messages = discover(args.app.strip(), args.scheduled)
        write_summary(messages, len(apps), args.scheduled)
        if args.preview:
            for path, kind, identity in apps:
                preview(path, kind, identity)
        elif not args.list:
            for path, kind, identity in apps:
                apply(path, kind, identity)
    except (OSError, ValueError, RuntimeError, urllib.error.URLError, yaml.YAMLError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
