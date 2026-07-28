#!/usr/bin/env python3
"""Apply explicitly supplied metadata to one Home Assistant app."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

import yaml
from packaging.version import InvalidVersion, Version

from update_apps import (
    APPS,
    Update,
    checkmk_app_version,
    load_app,
    replace_scalar,
    update_changelog,
)


def update_app(
    app: str,
    upstream_version: str,
    app_version: str,
    updated: str,
    commit: str,
    source: str,
    notes: str,
    apps_dir: Path = APPS,
) -> None:
    path = apps_dir / app
    if not path.is_dir():
        raise ValueError(f"Unknown app: {app}")
    config, var = load_app(path)
    if var.get("version_strategy") == "portainer_selector":
        raise ValueError(
            f"{app}: selector apps track LTS and STS together; use update_apps.py --app {app}"
        )
    if not app_version and var.get("version_strategy") == "checkmk_numeric_revision":
        app_version = checkmk_app_version(upstream_version, str(config.get("version") or ""))
    elif not app_version and var.get("version_strategy") == "upstream_revision":
        current = str(config.get("version") or "")
        prefix = f"{upstream_version}."
        revision = 0
        if current.startswith(prefix) and current[len(prefix) :].isdigit():
            revision = int(current[len(prefix) :])
        app_version = f"{upstream_version}.{revision + 1}"
    else:
        app_version = app_version or upstream_version
    if var.get("upstream_strategy") == "github_release_branch":
        if not re.fullmatch(r"\d+\.\d+\.\d+(?:p\d+)?", upstream_version) or not re.fullmatch(
            r"\d+\.\d+\.\d+\.\d+\.\d+", app_version
        ):
            raise ValueError(
                f"Invalid Checkmk version: upstream={upstream_version}, app={app_version}"
            )
    else:
        try:
            Version(upstream_version)
            Version(app_version)
        except InvalidVersion as error:
            raise ValueError(
                f"Invalid version: upstream={upstream_version}, app={app_version}"
            ) from error
    try:
        dt.date.fromisoformat(updated)
    except ValueError as error:
        raise ValueError(f"Invalid date (expected YYYY-MM-DD): {updated}") from error

    config_path, var_path = path / "config.yaml", path / ".var.yaml"
    config_text = replace_scalar(config_path.read_text(encoding="utf-8"), "version", app_version)
    var_text = var_path.read_text(encoding="utf-8")
    values = {
        "upstream_version": upstream_version,
        "upstream_commit": commit or str(var.get("upstream_commit", "")),
        "updated": updated,
        "source": source or str(var.get("source", "")),
    }
    for key, value in values.items():
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
            f"ARG UPSTREAM_VERSION={upstream_version}",
            docker_text,
            count=1,
        )
        if replacements != 1:
            raise ValueError(f"{app}: Dockerfile has no ARG UPSTREAM_VERSION")
        dockerfile.write_text(docker_text, encoding="utf-8", newline="\n")
    update_changelog(
        path / "CHANGELOG.md",
        Update(app_version, values["upstream_commit"], updated, values["source"], notes, "manual"),
    )
    print(
        f"UPDATED {app}: app {config.get('version', '')} -> {app_version}, "
        f"upstream {var.get('upstream_version', '')} -> {upstream_version}"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--app", required=True)
    parser.add_argument("--upstream-version", required=True)
    parser.add_argument("--app-version", default="")
    parser.add_argument("--updated", required=True)
    parser.add_argument("--commit", default="")
    parser.add_argument("--source", default="")
    parser.add_argument("--notes", default="Manuell aktualisierte Version.")
    args = parser.parse_args()
    try:
        update_app(
            args.app.strip(),
            args.upstream_version.strip(),
            args.app_version.strip(),
            args.updated.strip(),
            args.commit.strip(),
            args.source.strip(),
            args.notes.strip(),
        )
    except (OSError, ValueError, yaml.YAMLError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
