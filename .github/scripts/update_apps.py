#!/usr/bin/env python3
"""Update Home Assistant apps from GitHub releases, Docker Hub, or GHCR tags."""

from __future__ import annotations

import argparse
import datetime as dt
import functools
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

import yaml
from packaging.version import InvalidVersion, Version


ROOT = Path(__file__).resolve().parents[2]
APPS = ROOT / "apps"
USER_AGENT = "ha-app-autoupdater/1.0"
GITHUB_RE = re.compile(r"^(?:https?://)?github\.com/([^/]+)/([^/#]+?)(?:\.git)?/?$")
GHCR_RE = re.compile(r"^(?:https?://)?ghcr\.io/([^/]+)/([^/:@]+)(?::[^@]+)?$")
DOCKER_RE = re.compile(r"^(?:https?://)?(?:docker\.io/)?([^/]+)/([^/:@]+)(?::[^@]+)?$")
SEMVER_TAG_RE = re.compile(r"^v?\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
CHECKMK_BRANCH_RE = re.compile(r"^release/(?P<version>\d+\.\d+\.\d+(?:p\d+)?)$")


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
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.load(response), dict(response.headers.items())
        except urllib.error.HTTPError as error:
            if error.code != 429 or attempt == 3:
                raise
            retry_after = error.headers.get("Retry-After", "")
            delay = int(retry_after) if retry_after.isdigit() else 2 ** attempt
            print(f"RATE LIMITED: retrying {url} in {delay}s", file=sys.stderr)
            time.sleep(delay)
    raise RuntimeError(f"Unable to retrieve {url}")


def source_kind(value: str) -> tuple[str, tuple[str, str]] | None:
    value = value.strip()
    match = GITHUB_RE.match(value)
    if match:
        return "github", (match.group(1), match.group(2))
    match = GHCR_RE.match(value)
    if match:
        return "ghcr", (match.group(1), match.group(2))
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


def github_release_branch_update(owner: str, repository: str) -> Update:
    token = os.getenv("GITHUB_TOKEN", "")
    api = f"https://api.github.com/repos/{owner}/{repository}"
    branches: list[dict[str, Any]] = []
    page = 1
    while True:
        batch, _ = request_json(f"{api}/branches?per_page=100&page={page}", token)
        if not isinstance(batch, list):
            raise RuntimeError(f"github.com/{owner}/{repository}: invalid branch response")
        branches.extend(batch)
        if len(batch) < 100:
            break
        page += 1

    candidates = []
    for branch in branches:
        match = CHECKMK_BRANCH_RE.fullmatch(str(branch.get("name") or ""))
        if not match:
            continue
        version = match.group("version")
        numbers = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)(?:p(\d+))?", version)
        if numbers:
            major, minor, patch, patch_level = numbers.groups()
            candidates.append(
                ((int(major), int(minor), int(patch), int(patch_level or 0)), version, branch)
            )
    if not candidates:
        raise RuntimeError(f"github.com/{owner}/{repository}: no release/X.Y.Z[pN] branch found")

    _, version, branch = max(candidates, key=lambda item: item[0])
    commit = str((branch.get("commit") or {}).get("sha") or "")
    updated = dt.date.today().isoformat()
    commit_url = str((branch.get("commit") or {}).get("url") or "")
    if commit_url:
        try:
            details, _ = request_json(commit_url, token)
            updated = iso_date(
                ((details.get("commit") or {}).get("committer") or {}).get("date", "")
            )
        except (KeyError, urllib.error.HTTPError):
            pass
    source = f"github.com/{owner}/{repository}"
    return Update(
        version=version,
        commit=commit,
        updated=updated,
        source=source,
        notes=(
            f"- Checkmk release branch: `release/{version}`\n"
            f"- Agent source: `agents/check_mk_agent.openwrt`\n"
            f"- Commit: `{commit or 'nicht verfügbar'}`"
        ),
        kind="github",
    )


def semantic(tag: str) -> Version | None:
    if not SEMVER_TAG_RE.fullmatch(tag):
        return None
    try:
        version = Version(clean_version(tag))
        return version if not version.is_prerelease and not version.is_devrelease else None
    except InvalidVersion:
        return None


def docker_version(tag: str) -> Version | None:
    """Return the stable numeric version from a Docker tag variant."""
    match = re.fullmatch(r"v?(\d+\.\d+\.\d+)(?:[-+][0-9A-Za-z.-]+)?", tag)
    if not match:
        return None
    try:
        version = Version(match.group(1))
        return version if not version.is_prerelease and not version.is_devrelease else None
    except InvalidVersion:
        return None


def docker_digests(tag: dict[str, Any]) -> set[str]:
    """Collect manifest and platform image digests exposed by Docker Hub."""
    digests = {str(tag.get("digest") or "")}
    digests.update(str(image.get("digest") or "") for image in tag.get("images", []))
    digests.discard("")
    return digests


@functools.lru_cache(maxsize=None)
def docker_update(namespace: str, repository: str, tracking_tag: str = "latest") -> Update:
    base = (
        f"https://hub.docker.com/v2/namespaces/{namespace}"
        f"/repositories/{repository}/tags"
    )
    url = f"{base}?page_size=100&ordering=last_updated"
    tags: list[dict[str, Any]] = []
    page_number = 1
    while url and page_number <= 10:
        page, _ = request_json(url)
        tags.extend(page.get("results", []))
        url = page.get("next")
        page_number += 1

    latest = next((tag for tag in tags if tag.get("name") == tracking_tag), None)
    semver_tags = [(docker_version(tag.get("name", "")), tag) for tag in tags]
    semver_tags = [(version, tag) for version, tag in semver_tags if version is not None]
    if not semver_tags:
        raise RuntimeError(f"docker.io/{namespace}/{repository}: no semantic version tag found")

    same_digest = []
    if latest:
        tracked_digests = docker_digests(latest)
        same_digest = [
            item for item in semver_tags
            if tracked_digests.intersection(docker_digests(item[1]))
        ]
    if tracking_tag != "latest" and not latest:
        raise RuntimeError(
            f"docker.io/{namespace}/{repository}: tracking tag {tracking_tag!r} not found"
        )
    if tracking_tag != "latest" and not same_digest:
        raise RuntimeError(
            f"docker.io/{namespace}/{repository}: no version tag matches "
            f"tracking tag {tracking_tag!r} by manifest or platform digest"
        )
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
        version=str(version_obj),
        commit=digest,
        updated=iso_date(selected.get("last_updated", "")),
        source=source,
        notes=notes,
        kind="docker",
    )


class ChangelogParser(HTMLParser):
    """Convert the small HTML fragments returned by Homey's OTA API to Markdown."""

    def __init__(self) -> None:
        super().__init__()
        self.active = ""
        self.depth = 0
        self.buffer: list[str] = []
        self.lines: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if self.active:
            self.depth += 1
        elif tag in {"h2", "h3", "li", "p"}:
            self.active = tag
            self.depth = 1
            self.buffer = []

    def handle_data(self, data: str) -> None:
        if self.active:
            self.buffer.append(data)

    def handle_endtag(self, tag: str) -> None:
        if not self.active:
            return
        self.depth -= 1
        if self.depth:
            return
        text = re.sub(r"\s+", " ", html.unescape("".join(self.buffer))).strip()
        if text:
            if self.active in {"h2", "h3"}:
                self.lines.append(f"### {text}")
            elif self.active == "li":
                self.lines.append(f"- {text}")
            else:
                self.lines.append(text)
        self.active = ""
        self.buffer = []

    def markdown(self) -> str:
        return "\n".join(self.lines).strip()


def changelog_notes(url: str, version: str) -> str:
    request = urllib.request.Request(url, headers={"Accept": "text/html", "User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        document = response.read().decode("utf-8")
    if not re.search(r'<h2[^>]*class=["\'][^"\']*\bupdate-version\b', document, re.IGNORECASE):
        endpoint = re.search(r"""fetch\(\s*["'](https?://[^"']+)["']\s*\)""", document)
        if not endpoint:
            raise RuntimeError(f"{url}: no changelog endpoint found")
        request = urllib.request.Request(
            endpoint.group(1),
            headers={"Accept": "text/html", "User-Agent": USER_AGENT},
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            document = response.read().decode("utf-8")
    blocks = re.split(r'<div\s+class=["\']update["\']\s*>', document, flags=re.IGNORECASE)
    for block in blocks[1:]:
        match = re.search(
            r'<h2[^>]*class=["\']update-version["\'][^>]*>\s*v?([^<]+)</h2>',
            block,
            flags=re.IGNORECASE,
        )
        if not match or clean_version(match.group(1).strip()) != version:
            continue
        parser = ChangelogParser()
        parser.feed(block[match.end() :])
        return parser.markdown() or "Keine Release Notes vorhanden."
    return "Keine Release Notes für diese Version gefunden."


def ghcr_update(namespace: str, repository: str, changelog_url: str = "") -> Update:
    image = f"{namespace}/{repository}"
    query = urllib.parse.urlencode({"service": "ghcr.io", "scope": f"repository:{image}:pull"})
    token_data, _ = request_json(f"https://ghcr.io/token?{query}")
    token = token_data.get("token", "")
    if not token:
        raise RuntimeError(f"ghcr.io/{image}: registry token missing")
    headers = {
        "Accept": "application/vnd.oci.image.index.v1+json, application/vnd.docker.distribution.manifest.list.v2+json",
        "Authorization": f"Bearer {token}",
        "User-Agent": USER_AGENT,
    }
    tags_request = urllib.request.Request(f"https://ghcr.io/v2/{image}/tags/list?n=1000", headers=headers)
    with urllib.request.urlopen(tags_request, timeout=30) as response:
        tags = json.load(response).get("tags", [])
    versions = [(semantic(tag), tag) for tag in tags]
    versions = [(version, tag) for version, tag in versions if version is not None]
    if not versions:
        raise RuntimeError(f"ghcr.io/{image}: no semantic version tag found")
    version_obj, tag = max(versions, key=lambda item: item[0])
    manifest_request = urllib.request.Request(
        f"https://ghcr.io/v2/{image}/manifests/{urllib.parse.quote(tag, safe='')}",
        headers=headers,
        method="HEAD",
    )
    with urllib.request.urlopen(manifest_request, timeout=30) as response:
        digest = response.headers.get("Docker-Content-Digest", "")
    version = str(version_obj)
    source = f"ghcr.io/{image}"
    if changelog_url:
        notes = f"{changelog_notes(changelog_url, version)}\n\nRelease Notes: {changelog_url}"
    else:
        notes = f"- GHCR image: `{source}:{tag}`\n- Digest: `{digest or 'nicht verfügbar'}`"
    return Update(
        version=version,
        commit=digest,
        updated=dt.date.today().isoformat(),
        source=source,
        notes=notes,
        kind="ghcr",
    )


def fetch_update(path: Path, kind: str, identity: tuple[str, str]) -> Update:
    _, var = load_app(path)
    raw_source = str(var.get("upstream_repo") or var.get("source") or "")
    if var.get("upstream_strategy") == "github_release_branch":
        if kind != "github":
            raise ValueError(f"{path.name}: github_release_branch requires a GitHub source")
        return github_release_branch_update(*identity)
    if kind == "github":
        return github_update(*identity, raw_source)
    if kind == "docker":
        return docker_update(*identity, str(var.get("upstream_tracking_tag") or "latest"))
    return ghcr_update(*identity, str(var.get("changelog_url") or ""))


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
    elif update.kind == "ghcr":
        entry += f"### GitHub Container Registry\n\n{update.notes}\n"
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


def calendar_revision(current: str, today: dt.date) -> str:
    prefix = f"{today.year}.{today.month}."
    revision = 0
    if current.startswith(prefix):
        suffix = current[len(prefix) :]
        if suffix.isdigit():
            revision = int(suffix)
    return f"{prefix}{revision + 1}"


def checkmk_app_version(upstream: str, current: str) -> str:
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)(?:p(\d+))?", upstream)
    if not match:
        raise ValueError(f"Invalid Checkmk upstream version: {upstream}")
    major, minor, patch, patch_level = match.groups()
    prefix = f"{major}.{minor}.{patch}.{patch_level or '0'}."
    revision = 0
    if current.startswith(prefix) and current[len(prefix) :].isdigit():
        revision = int(current[len(prefix) :])
    return f"{prefix}{revision + 1}"


def bump_app_revision(path: Path) -> str:
    """Increase only the Home Assistant app revision for a forced rebuild."""
    config, var = load_app(path)
    current = str(config.get("version") or "")
    upstream = str(var.get("upstream_version") or "")
    strategy = str(var.get("version_strategy") or "")

    if strategy == "portainer_selector":
        bumped = calendar_revision(current, dt.date.today())
    elif strategy == "checkmk_numeric_revision":
        bumped = checkmk_app_version(upstream, current)
    else:
        prefix = f"{upstream}."
        if current == upstream:
            bumped = f"{upstream}.1"
        elif current.startswith(prefix) and current[len(prefix) :].isdigit():
            bumped = f"{prefix}{int(current[len(prefix):]) + 1}"
        else:
            raise ValueError(
                f"{path.name}: app version {current!r} does not match "
                f"upstream version {upstream!r}"
            )

    config_path = path / "config.yaml"
    config_text = replace_scalar(config_path.read_text(encoding="utf-8"), "version", bumped)
    yaml.safe_load(config_text)
    config_path.write_text(config_text, encoding="utf-8", newline="\n")
    update_changelog(
        path / "CHANGELOG.md",
        Update(
            version=bumped,
            commit=str(var.get("upstream_commit") or ""),
            updated=dt.date.today().isoformat(),
            source=str(var.get("source") or ""),
            notes="- App-Revision für einen vollständigen Neuaufbau um eins erhöht.",
            kind="manual",
        ),
    )
    print(f"BUMPED {path.name}: {current} -> {bumped}")
    return bumped


def selector_changelog(
    path: Path,
    app_version: str,
    updated: str,
    old_lts: str,
    new_lts: Update,
    old_sts: str,
    new_sts: Update,
    old_secondary_lts: str = "",
    secondary_lts: Update | None = None,
    old_secondary_sts: str = "",
    secondary_sts: Update | None = None,
) -> None:
    primary_lts_changed = old_lts != new_lts.version
    primary_sts_changed = old_sts != new_sts.version
    lts_changed = primary_lts_changed or bool(
        secondary_lts and old_secondary_lts != secondary_lts.version
    )
    sts_changed = primary_sts_changed or bool(
        secondary_sts and old_secondary_sts != secondary_sts.version
    )
    changes = []
    if primary_lts_changed:
        changes.append(f"- LTS: `{old_lts or 'nicht gesetzt'}` → `{new_lts.version}`")
    if primary_sts_changed:
        changes.append(f"- STS: `{old_sts or 'nicht gesetzt'}` → `{new_sts.version}`")
    if secondary_lts and old_secondary_lts != secondary_lts.version:
        changes.append(
            f"- EE LTS: `{old_secondary_lts or 'nicht gesetzt'}` → `{secondary_lts.version}`"
        )
    if secondary_sts and old_secondary_sts != secondary_sts.version:
        changes.append(
            f"- EE STS: `{old_secondary_sts or 'nicht gesetzt'}` → `{secondary_sts.version}`"
        )
    if not changes:
        changes.append("- Keine Versionsänderung; Docker-Image-Digest wurde aktualisiert.")
    lts_line = (
        f"- LTS: `CE {new_lts.version}, EE {secondary_lts.version}`"
        if secondary_lts
        else f"- LTS: `{new_lts.version}`"
    )
    sts_line = (
        f"- STS: `CE {new_sts.version}, EE {secondary_sts.version}`"
        if secondary_sts
        else f"- STS: `{new_sts.version}`"
    )
    entry = (
        f"## [{app_version}] - {updated}\n\n"
        "### Enthaltene Upstream-Versionen\n\n"
        + lts_line
        + ("\n" if lts_changed else " (keine Änderung)\n")
        + sts_line
        + ("\n" if sts_changed else " (keine Änderung)\n")
        + "\n### Änderungen\n\n"
        + "\n".join(changes)
        + "\n\n---\n"
    )
    changelog = path / "CHANGELOG.md"
    original = changelog.read_text(encoding="utf-8") if changelog.exists() else "# Changelog\n"
    header = re.match(r"(?s)^(# .+?\n)(?:\n)?", original)
    result = (
        original[: header.end()] + "\n" + entry + "\n" + original[header.end() :].lstrip("\n")
        if header
        else "# Changelog\n\n" + entry + "\n" + original
    )
    changelog.write_text(result, encoding="utf-8", newline="\n")


def apply_portainer_selector(path: Path, config: dict[str, Any], var: dict[str, Any]) -> bool:
    raw_source = str(var.get("upstream_repo") or var.get("source") or "")
    parsed = source_kind(raw_source)
    if not parsed or parsed[0] != "docker":
        raise ValueError(f"{path.name}: selector requires a Docker Hub upstream_repo")
    namespace, repository = parsed[1]
    lts = docker_update(namespace, repository, str(var.get("lts_tracking_tag") or "alpine"))
    sts = docker_update(namespace, repository, str(var.get("sts_tracking_tag") or "alpine-sts"))
    secondary_lts = secondary_sts = None
    secondary_source = str(var.get("selector_secondary_repo") or "")
    if secondary_source:
        secondary_parsed = source_kind(secondary_source)
        if not secondary_parsed or secondary_parsed[0] != "docker":
            raise ValueError(f"{path.name}: selector_secondary_repo must be a Docker Hub image")
        secondary_lts = docker_update(
            *secondary_parsed[1], str(var.get("lts_tracking_tag") or "alpine")
        )
        secondary_sts = docker_update(
            *secondary_parsed[1], str(var.get("sts_tracking_tag") or "alpine-sts")
        )
    old_lts = str(var.get("lts_version") or "")
    old_sts = str(var.get("sts_version") or "")
    if (
        old_lts == lts.version
        and old_sts == sts.version
        and str(var.get("lts_commit") or "") == lts.commit
        and str(var.get("sts_commit") or "") == sts.commit
        and (not secondary_lts or str(var.get("secondary_lts_commit") or "") == secondary_lts.commit)
        and (not secondary_sts or str(var.get("secondary_sts_commit") or "") == secondary_sts.commit)
    ):
        print(f"UNCHANGED {path.name}: LTS {lts.version}, STS {sts.version}")
        return False

    today = dt.date.today()
    app_version = calendar_revision(str(config.get("version") or ""), today)
    config_path, var_path = path / "config.yaml", path / ".var.yaml"
    config_text = replace_scalar(config_path.read_text(encoding="utf-8"), "version", app_version)
    var_text = var_path.read_text(encoding="utf-8")
    for key, value in (
        ("upstream_version", sts.version),
        ("upstream_commit", sts.commit),
        ("lts_version", lts.version),
        ("lts_commit", lts.commit),
        ("sts_version", sts.version),
        ("sts_commit", sts.commit),
        ("updated", today.isoformat()),
        ("source", sts.source),
    ):
        var_text = replace_scalar(var_text, key, value)
    if secondary_lts and secondary_sts:
        for key, value in (
            ("secondary_lts_version", secondary_lts.version),
            ("secondary_lts_commit", secondary_lts.commit),
            ("secondary_sts_version", secondary_sts.version),
            ("secondary_sts_commit", secondary_sts.commit),
        ):
            var_text = replace_scalar(var_text, key, value)

    if path.name not in {"portainer", "portainer-agent"}:
        raise ValueError(f"Unsupported selector app: {path.name}")

    yaml.safe_load(config_text)
    yaml.safe_load(var_text)
    config_path.write_text(config_text, encoding="utf-8", newline="\n")
    var_path.write_text(var_text, encoding="utf-8", newline="\n")
    selector_changelog(
        path, app_version, today.isoformat(), old_lts, lts, old_sts, sts,
        str(var.get("secondary_lts_version") or ""), secondary_lts,
        str(var.get("secondary_sts_version") or ""), secondary_sts,
    )
    print(
        f"UPDATED {path.name}: {config.get('version', '')} -> {app_version}; "
        f"LTS {old_lts or '-'} -> {lts.version}; STS {old_sts or '-'} -> {sts.version}"
    )
    return True


def apply(path: Path, kind: str, identity: tuple[str, str]) -> bool:
    config, var = load_app(path)
    if var.get("version_strategy") == "portainer_selector":
        return apply_portainer_selector(path, config, var)
    update = fetch_update(path, kind, identity)
    current_upstream_version = str(var.get("upstream_version", ""))
    if (
        current_upstream_version == update.version
        and str(var.get("upstream_commit", "")) == update.commit
    ):
        print(f"UNCHANGED {path.name}: {update.version}")
        return False

    if var.get("version_strategy") == "checkmk_numeric_revision":
        app_version = checkmk_app_version(update.version, str(config.get("version") or ""))
    elif current_upstream_version == update.version:
        current_app_version = str(config.get("version", ""))
        revision_prefix = f"{update.version}."
        revision = 0
        if current_app_version.startswith(revision_prefix):
            revision_text = current_app_version[len(revision_prefix) :]
            if revision_text.isdigit():
                revision = int(revision_text)
        app_version = f"{update.version}.{revision + 1}"
    elif var.get("version_strategy") == "upstream_revision":
        app_version = f"{update.version}.1"
    else:
        app_version = update.version

    config_path, var_path = path / "config.yaml", path / ".var.yaml"
    config_text = replace_scalar(config_path.read_text(encoding="utf-8"), "version", app_version)
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
    if var.get("version_strategy") in {"upstream_revision", "checkmk_numeric_revision"}:
        dockerfile = path / "Dockerfile"
        docker_text = dockerfile.read_text(encoding="utf-8")
        docker_text, replacements = re.subn(
            r"(?m)^ARG UPSTREAM_VERSION=.*$",
            f"ARG UPSTREAM_VERSION={update.version}",
            docker_text,
            count=1,
        )
        if replacements != 1:
            raise ValueError(f"{path.name}: Dockerfile has no ARG UPSTREAM_VERSION")
        dockerfile.write_text(docker_text, encoding="utf-8", newline="\n")
    update_changelog(
        path / "CHANGELOG.md",
        Update(
            app_version,
            update.commit,
            update.updated,
            update.source,
            update.notes,
            update.kind,
        ),
    )
    print(f"UPDATED {path.name}: {config.get('version', '')} -> {app_version}")
    return True


def preview(path: Path, kind: str, identity: tuple[str, str]) -> None:
    """Fetch and display an update without changing repository files."""
    config, var = load_app(path)
    if var.get("version_strategy") == "portainer_selector":
        namespace, repository = identity
        lts = docker_update(namespace, repository, str(var.get("lts_tracking_tag") or "alpine"))
        sts = docker_update(namespace, repository, str(var.get("sts_tracking_tag") or "alpine-sts"))
        body = (
            f"## Update-Vorschau: `{path.name}`\n\n"
            "| Kanal | Aktuell | Ermittelt |\n"
            "|---|---|---|\n"
            f"| LTS | `{var.get('lts_version', '')}` | `{lts.version}` |\n"
            f"| STS | `{var.get('sts_version', '')}` | `{sts.version}` |\n"
            f"| Nächste App-Version | `{config.get('version', '')}` | "
            f"`{calendar_revision(str(config.get('version') or ''), dt.date.today())}` |\n"
        )
        print(body)
        if summary := os.getenv("GITHUB_STEP_SUMMARY"):
            with open(summary, "a", encoding="utf-8") as handle:
                handle.write(body)
        return
    update = fetch_update(path, kind, identity)
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
    parser.add_argument(
        "--bump-revision",
        action="store_true",
        help="increase each selected Home Assistant app revision after update detection",
    )
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
            if args.bump_revision:
                for path, _, _ in apps:
                    bump_app_revision(path)
    except (OSError, ValueError, RuntimeError, urllib.error.URLError, yaml.YAMLError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
