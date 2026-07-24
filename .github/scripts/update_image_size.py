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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True, help="Published image reference including tag")
    parser.add_argument("--var-file", required=True, type=Path)
    parser.add_argument("--attempts", type=int, default=6)
    args = parser.parse_args()

    error: Exception | None = None
    for attempt in range(args.attempts):
        try:
            sizes = manifest_sizes(args.image, inspect_manifest(args.image))
            if not sizes:
                raise RuntimeError(f"No platform image layers found for {args.image}")
            value = format_size(max(sizes))
            changed = update_var_file(args.var_file, value)
            print(f"{args.image}: {value} ({'updated' if changed else 'unchanged'})")
            return
        except (json.JSONDecodeError, RuntimeError, subprocess.CalledProcessError) as exc:
            error = exc
            if attempt + 1 < args.attempts:
                time.sleep(2**attempt)
    raise RuntimeError(f"Unable to inspect {args.image} after {args.attempts} attempts") from error


if __name__ == "__main__":
    main()
