#!/usr/bin/env python3
"""Update image_size from the compressed layers in a registry manifest."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import time
from pathlib import Path
from typing import Any


IMAGE_SIZE_PATTERN = re.compile(
    r'^(?P<prefix>[ \t]*image_size[ \t]*:[ \t]*)(?P<quote>["\']?)(?P<value>.*?)(?P=quote)(?P<suffix>[ \t]*)$',
    re.MULTILINE,
)


def inspect_manifest(reference: str) -> dict[str, Any]:
    result = subprocess.run(
        ["docker", "buildx", "imagetools", "inspect", "--raw", reference],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def manifest_sizes(reference: str, manifest: dict[str, Any]) -> list[int]:
    layers = manifest.get("layers")
    if isinstance(layers, list):
        return [sum(int(layer.get("size", 0)) for layer in layers)]

    sizes: list[int] = []
    image = reference.split("@", 1)[0].rsplit(":", 1)[0]
    for descriptor in manifest.get("manifests", []):
        platform = descriptor.get("platform", {})
        if platform.get("architecture") in (None, "unknown"):
            continue
        digest = descriptor.get("digest")
        if digest:
            child_reference = f"{image}@{digest}"
            sizes.extend(manifest_sizes(child_reference, inspect_manifest(child_reference)))
    return sizes


def format_size(size: int) -> str:
    megabytes = size / 1_000_000
    if megabytes >= 10:
        return f"{megabytes:.0f} MB"
    return f"{megabytes:.1f} MB"


def update_var_file(path: Path, value: str) -> bool:
    content = path.read_text(encoding="utf-8")
    match = IMAGE_SIZE_PATTERN.search(content)
    if not match:
        raise ValueError(f"{path} has no image_size field")
    replacement = f'{match.group("prefix")}"{value}"{match.group("suffix")}'
    updated = content[: match.start()] + replacement + content[match.end() :]
    if updated == content:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def write_result(path: Path, app: str, value: str) -> None:
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", app):
        raise ValueError(f"Invalid app slug: {app!r}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"app": app, "image_size": value}, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def apply_results(directory: Path, apps_root: Path = Path("apps")) -> int:
    result_files = sorted(directory.glob("*.json"))
    if not result_files:
        raise ValueError(f"No image-size results found in {directory}")

    changed_count = 0
    for result_file in result_files:
        result = json.loads(result_file.read_text(encoding="utf-8"))
        app = result.get("app", "")
        value = result.get("image_size", "")
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", app):
            raise ValueError(f"Invalid app slug in {result_file}: {app!r}")
        if not re.fullmatch(r"\d+(?:\.\d+)? MB", value):
            raise ValueError(f"Invalid image size in {result_file}: {value!r}")

        var_file = apps_root / app / ".var.yaml"
        if not var_file.is_file():
            raise ValueError(f"Unknown app in {result_file}: {app}")
        changed = update_var_file(var_file, value)
        changed_count += int(changed)
        print(f"{app}: {value} ({'updated' if changed else 'unchanged'})")
    return changed_count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", help="Published image reference including tag")
    parser.add_argument("--var-file", type=Path)
    parser.add_argument("--result-file", type=Path)
    parser.add_argument("--app", help="App slug stored in --result-file")
    parser.add_argument("--apply-results", type=Path)
    parser.add_argument("--attempts", type=int, default=6)
    args = parser.parse_args()

    if args.apply_results:
        if args.image or args.var_file or args.result_file or args.app:
            parser.error("--apply-results cannot be combined with image inspection options")
        apply_results(args.apply_results)
        return

    if not args.image:
        parser.error("--image is required unless --apply-results is used")
    if not args.var_file and not args.result_file:
        parser.error("either --var-file or --result-file is required")
    if args.result_file and not args.app:
        parser.error("--app is required with --result-file")

    error: Exception | None = None
    for attempt in range(args.attempts):
        try:
            sizes = manifest_sizes(args.image, inspect_manifest(args.image))
            if not sizes:
                raise RuntimeError(f"No platform image layers found for {args.image}")
            value = format_size(max(sizes))
            changed = update_var_file(args.var_file, value) if args.var_file else False
            if args.result_file:
                write_result(args.result_file, args.app, value)
            status = "updated" if changed else "collected" if args.result_file else "unchanged"
            print(f"{args.image}: {value} ({status})")
            return
        except (json.JSONDecodeError, RuntimeError, subprocess.CalledProcessError) as exc:
            error = exc
            if attempt + 1 < args.attempts:
                time.sleep(2**attempt)
    raise RuntimeError(f"Unable to inspect {args.image} after {args.attempts} attempts") from error


if __name__ == "__main__":
    main()
