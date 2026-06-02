"""Check that CLI/skill code doesn't contain forbidden network calls."""

import re
import sys
from pathlib import Path

FORBIDDEN_PATTERNS = [
    (re.compile(r"requests\.(get|post|put|delete|patch|head)\s*\("), "requests HTTP call"),
    (re.compile(r"urllib\.request\.urlopen\s*\("), "urllib network call"),
    (re.compile(r"httpx\.(get|post|put|delete|patch|head)\s*\("), "httpx HTTP call"),
    (re.compile(r"aiohttp\.\w+\.\w+\.\w+\s*\("), "aiohttp network call"),
    (re.compile(r"socket\.connect\s*\("), "raw socket connection"),
]

# Exceptions: imports and type hints are OK
SAFE_PATTERNS = [
    re.compile(r"^\s*import\s"),
    re.compile(r"^\s*from\s"),
    re.compile(r"^\s*#"),
]


def check_file(path: Path) -> list[str]:
    """Check a file for forbidden network calls."""
    issues = []
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return issues

    for line_num, line in enumerate(text.splitlines(), 1):
        if any(p.search(line) for p in SAFE_PATTERNS):
            continue
        for pattern, desc in FORBIDDEN_PATTERNS:
            if pattern.search(line):
                issues.append(f"  {path}:{line_num} — {desc}: {line.strip()}")
    return issues


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: check_no_forbidden_network_calls.py <dir1> [dir2] ...")
        return 1

    all_issues: list[str] = []
    for arg in sys.argv[1:]:
        root = Path(arg)
        if not root.exists():
            continue
        for path in root.rglob("*.py"):
            all_issues.extend(check_file(path))

    if all_issues:
        print(f"Found {len(all_issues)} forbidden network calls:")
        for issue in all_issues:
            print(issue)
        return 1

    print("No forbidden network calls found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
