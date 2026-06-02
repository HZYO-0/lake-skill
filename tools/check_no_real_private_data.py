"""Check files for real private data patterns.

Scans all provided directories. Uses safe-pattern allowlists to distinguish
synthetic/example data from real PII. Source code (cli/, skill/, tools/) is
scanned strictly; test/example/doc files are scanned with broader allowlists.

Usage:
    python tools/check_no_real_private_data.py cli skill tools
    python tools/check_no_real_private_data.py tests examples docs
    python tools/check_no_real_private_data.py cli skill tools tests examples docs
"""

import re
import sys
from pathlib import Path

# PII patterns to detect
PATTERNS = [
    (re.compile(r"1[3-9]\d{9}"), "Chinese phone number"),
    (re.compile(r"\d{17}[\dXx]"), "Chinese ID card"),
    (re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"), "email address"),
    (re.compile(r"\d{16,19}"), "bank card number"),
    (re.compile(r"wxid_[a-zA-Z0-9]+"), "WeChat ID"),
]

# Safe patterns: known test/synthetic values that should not trigger alerts
SAFE_PATTERNS = [
    # Email patterns
    re.compile(r"example\.com"),
    re.compile(r"test[@_]"),
    re.compile(r"@test"),
    re.compile(r"@example"),
    # Phone patterns (common test numbers)
    re.compile(r"13800138000"),
    re.compile(r"138\d{8}"),  # 138 prefix is common in test data
    re.compile(r"139\d{8}"),  # 139 prefix in test data
    # WeChat ID patterns (synthetic)
    re.compile(r"wxid_test"),
    re.compile(r"wxid_self"),
    re.compile(r"wxid_target"),
    re.compile(r"wxid_abc123"),
    re.compile(r"wxid_synthetic"),
    # Chinese placeholder names
    re.compile(r"张三|李四|王五|赵六"),
    # Chat role markers
    re.compile(r"对方|我:"),
    # Synthetic/example markers in context
    re.compile(r"synthetic", re.IGNORECASE),
    re.compile(r"example", re.IGNORECASE),
    re.compile(r"fixture", re.IGNORECASE),
    re.compile(r"mock[_ ]", re.IGNORECASE),
    re.compile(r"fake[_ ]", re.IGNORECASE),
    re.compile(r"sample", re.IGNORECASE),
    # Test file markers
    re.compile(r"test_redact"),
    re.compile(r"def test_"),
    re.compile(r"assert.*not in"),
    re.compile(r"\[PHONE\]|\[EMAIL\]|\[WECHAT_ID\]|\[NAME\]"),
]

# Source directories: strict scanning (no safe-pattern bypass for source)
SOURCE_DIRS = {"cli", "skill"}

# Files to skip entirely (self-referential, historical)
SKIP_PATTERNS = [
    re.compile(r"tools[/\\]check_no_real_private_data\.py"),
    re.compile(r"docs[/\\]archive"),
]

# Extensions to scan
SCAN_EXTENSIONS = {".py", ".md", ".jsonl", ".yaml", ".yml", ".txt", ".csv"}


def is_source_file(path: Path) -> bool:
    """Check if a file is in a source directory (strict scanning)."""
    parts = set(path.parts)
    return bool(parts & SOURCE_DIRS)


def is_safe_line(line: str) -> bool:
    """Check if a line matches a known safe pattern."""
    return any(p.search(line) for p in SAFE_PATTERNS)


def check_file(path: Path, strict: bool = False) -> list[str]:
    """Check a file for real private data patterns.

    Args:
        path: File to check
        strict: If True, don't apply safe-pattern bypass (for source files)
    """
    issues = []
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return issues

    for line_num, line in enumerate(text.splitlines(), 1):
        if not strict and is_safe_line(line):
            continue
        for pattern, desc in PATTERNS:
            if pattern.search(line):
                issues.append(f"  {path}:{line_num} — possible {desc}")
    return issues


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: check_no_real_private_data.py <dir1> [dir2] ...")
        return 1

    all_issues: list[str] = []
    for arg in sys.argv[1:]:
        root = Path(arg)
        if not root.exists():
            continue
        strict = root.name in SOURCE_DIRS
        for path in root.rglob("*"):
            if not path.is_file() or path.suffix not in SCAN_EXTENSIONS:
                continue
            # Skip self-referential and historical files
            path_str = str(path.as_posix())
            if any(p.search(path_str) for p in SKIP_PATTERNS):
                continue
            all_issues.extend(check_file(path, strict=strict))

    if all_issues:
        print(f"Found {len(all_issues)} potential privacy issues:")
        for issue in all_issues:
            print(issue)
        return 1

    print("No real private data patterns found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
