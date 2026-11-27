#!/usr/bin/env python3
"""Synchronize standalone slide bundles from _shared; check by default."""

import argparse
import hashlib
import json
from pathlib import Path
import sys


GROUP = Path(__file__).resolve().parents[1]
SKILLS = ("slide-share", "slide-survey", "slide-tech")
MANIFEST = ".common-manifest.json"


def digest(content):
    return hashlib.sha256(content).hexdigest()


def snapshot(root):
    files = {}
    if root.is_symlink():
        raise ValueError(f"refuse symlinked directory: {root}")
    if not root.exists():
        return files
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"refuse symlink: {path}")
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        if path.is_file() and path.relative_to(root).as_posix() != MANIFEST:
            files[path.relative_to(root).as_posix()] = path.read_bytes()
    return files


def plan(skill, desired):
    target = GROUP / skill / "common"
    if not (target.parent / "SKILL.md").is_file():
        raise ValueError(f"missing skill entry: {skill}")
    current = snapshot(target)
    manifest_path = target / MANIFEST
    if manifest_path.is_symlink():
        raise ValueError(f"refuse symlinked manifest: {manifest_path}")
    previous = {}
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if not isinstance(manifest, dict) or manifest.get("schema_version") != 1:
            raise ValueError(f"invalid generated manifest: {manifest_path}")
        previous = manifest.get("files")
        if not isinstance(previous, dict):
            raise ValueError(f"invalid manifest files: {manifest_path}")
    for name, content in current.items():
        # Never overwrite an unowned file, even if it happens to match the source.
        if name not in previous:
            raise ValueError(f"unmanaged common file; inspect before syncing: {target / name}")
        if digest(content) != previous[name] and content != desired.get(name):
            raise ValueError(f"modified generated file; preserve changes first: {target / name}")
    expected = {name: digest(content) for name, content in desired.items()}
    changed = current != desired or previous != expected
    return target, current, expected, changed


def synchronize(write=False):
    source = GROUP / "_shared"
    desired = snapshot(source)
    if not desired or any(Path(name).parts[0] not in {"references", "scripts", "assets"} for name in desired):
        raise ValueError("_shared must contain only references/, scripts/, and assets/ resources")
    if any(Path(name).name == "SKILL.md" for name in desired):
        raise ValueError("_shared must not contain discoverable skill entries")
    # Validate all targets before writing any bundle.
    plans = [(skill, *plan(skill, desired)) for skill in SKILLS]
    out_of_sync = []
    for skill, target, current, expected, changed in plans:
        if not changed:
            print(f"OK: {skill}/common")
            continue
        out_of_sync.append(skill)
        if not write:
            print(f"OUT OF SYNC: {skill}/common")
            continue
        target.mkdir(parents=True, exist_ok=True)
        for name in current.keys() - desired.keys():
            (target / name).unlink()  # Only unchanged, manifest-owned stale files.
        for name, content in desired.items():
            path = target / name
            path.parent.mkdir(parents=True, exist_ok=True)
            if current.get(name) != content:
                path.write_bytes(content)
        (target / MANIFEST).write_text(
            json.dumps({"schema_version": 1, "files": expected}, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(f"SYNCED: {skill}/common")
    return not out_of_sync or write


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="report drift without writing (default)")
    mode.add_argument("--write", action="store_true", help="update only managed generated bundles")
    args = parser.parse_args()
    try:
        return 0 if synchronize(write=args.write) else 1
    except (ValueError, OSError) as error:
        print(f"Sync failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
