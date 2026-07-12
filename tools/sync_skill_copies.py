"""Synchronize generated platform copies from the canonical skills/lake-skill tree."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills" / "lake-skill"
TARGETS = (
    ROOT / ".codex" / "skills" / "lake-skill",
    ROOT / ".claude" / "skills" / "lake-skill",
    ROOT / ".opencode" / "skills" / "lake-skill",
    ROOT / ".agents" / "skills" / "lake-skill",
)
MANIFEST = ".skill-manifest.json"


def tree_manifest(root: Path) -> dict:
    files = {}
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.name != MANIFEST:
            relative = path.relative_to(root).as_posix()
            files[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    encoded = json.dumps(files, sort_keys=True, separators=(",", ":")).encode()
    return {"tree_hash": hashlib.sha256(encoded).hexdigest(), "files": files}


def write_manifest(root: Path) -> dict:
    manifest = tree_manifest(root)
    (root / MANIFEST).write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return manifest


def sync() -> None:
    canonical = write_manifest(SOURCE)
    for target in TARGETS:
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(SOURCE, target)
        (target / MANIFEST).write_text(
            json.dumps(canonical, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        print(f"synced {target.relative_to(ROOT)} {canonical['tree_hash'][:12]}")


def check() -> int:
    expected = tree_manifest(SOURCE)
    failures = []
    for target in TARGETS:
        if not target.exists() or tree_manifest(target) != expected:
            failures.append(str(target.relative_to(ROOT)))
    if failures:
        print("skill copy drift: " + ", ".join(failures))
        return 1
    print(f"skill copies match {expected['tree_hash']}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        return check()
    sync()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
