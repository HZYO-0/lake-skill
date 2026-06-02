"""Leak checker for privacy validation."""

import re
from pathlib import Path
from typing import Optional

from .modes import PrivacyMode


# Patterns to detect real data leaks
LEAK_PATTERNS = {
    "phone": re.compile(r"1[3-9]\d{9}"),
    "id_card": re.compile(r"[1-9]\d{5}(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx]"),
    "email": re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"),
    "wechat_id": re.compile(r"wxid_[a-zA-Z0-9_]{6,20}"),
    "bank_card": re.compile(r"\d{16,19}"),
}


class LeakChecker:
    """Check for privacy leaks in files."""

    def __init__(self, mode: PrivacyMode = PrivacyMode.CLOUD_SAFE) -> None:
        """Initialize leak checker.

        Args:
            mode: Privacy mode to check against
        """
        self.mode = mode
        self.leaks: list[dict] = []

    def check_file(self, file_path: Path) -> list[dict]:
        """Check a file for privacy leaks.

        Args:
            file_path: Path to file to check

        Returns:
            List of detected leaks
        """
        leaks = []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Check for each pattern
            for pattern_name, pattern in LEAK_PATTERNS.items():
                matches = pattern.findall(content)
                if matches:
                    for match in matches:
                        # Skip redacted markers
                        if match.startswith("[") and match.endswith("]"):
                            continue
                        leaks.append({
                            "file": str(file_path),
                            "pattern": pattern_name,
                            "match": match[:10] + "..." if len(match) > 10 else match,
                        })

        except Exception as e:
            leaks.append({
                "file": str(file_path),
                "pattern": "error",
                "match": str(e),
            })

        self.leaks.extend(leaks)
        return leaks

    def check_directory(self, dir_path: Path, extensions: Optional[list[str]] = None) -> list[dict]:
        """Check all files in a directory for privacy leaks.

        Args:
            dir_path: Path to directory to check
            extensions: File extensions to check (default: common text files)

        Returns:
            List of detected leaks
        """
        if extensions is None:
            extensions = [".md", ".txt", ".json", ".jsonl", ".yaml", ".yml", ".csv"]

        all_leaks = []

        for ext in extensions:
            for file_path in dir_path.rglob(f"*{ext}"):
                # Skip test fixtures and examples
                if "fixtures" in str(file_path) or "synthetic" in str(file_path):
                    continue
                leaks = self.check_file(file_path)
                all_leaks.extend(leaks)

        return all_leaks

    def has_leaks(self) -> bool:
        """Check if any leaks were detected."""
        return len(self.leaks) > 0

    def get_report(self) -> str:
        """Get a report of detected leaks.

        Returns:
            Report string
        """
        if not self.leaks:
            return "No privacy leaks detected."

        report_lines = [f"Found {len(self.leaks)} potential privacy leaks:\n"]
        for leak in self.leaks:
            report_lines.append(
                f"  - {leak['file']}: {leak['pattern']} = {leak['match']}"
            )

        return "\n".join(report_lines)


def check_for_leaks(
    dir_path: Path,
    mode: PrivacyMode = PrivacyMode.CLOUD_SAFE,
) -> tuple[bool, str]:
    """Check directory for privacy leaks.

    Args:
        dir_path: Path to directory to check
        mode: Privacy mode to check against

    Returns:
        Tuple of (has_leaks, report)
    """
    checker = LeakChecker(mode)
    checker.check_directory(dir_path)
    return checker.has_leaks(), checker.get_report()
