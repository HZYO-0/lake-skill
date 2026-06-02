"""Check model output against expected structural requirements.

Validates that Skill output meets minimum structural requirements for
each scenario (sparse, representative, cli_export).

Usage:
    python tools/check_expected_output.py --scenario sparse output.md
    python tools/check_expected_output.py --scenario representative output.md
    python tools/check_expected_output.py --scenario cli_export output.md
"""

import argparse
import re
import sys
from pathlib import Path

# Scenario requirements: (must_contain_patterns, must_not_contain_patterns)
SCENARIOS = {
    "sparse": {
        "must_contain": [
            r"不(足|够|充分)",  # data insufficient
            r"(需要|建议|提供).*更?多",  # need more data
        ],
        "must_not_contain": [
            r"(关系|沟通)画像",  # full portrait
            r"(大五|人格).*(信号|报告|分析)",  # personality report
            r"依恋.*(假设|报告|分析)",  # attachment report
            r"沟通手册",  # playbook
            r"(草稿|draft).*消息",  # message drafts
            r"(他|她|对方)一定是",  # certainty language
            r"(他|她|对方)肯定",  # certainty language
            r"(他|她|对方)就是.*型",  # type diagnosis
            r"(回避型|焦虑型).*(人格|依恋).*(障碍|诊断)",  # clinical diagnosis
        ],
    },
    "representative": {
        "must_contain": [
            r"证据",  # evidence reference
            r"置信度|confidence",  # confidence level
            r"替代解释|alternative",  # alternative explanation
            r"反证|counterevidence|未发现.*反证",  # counterevidence or none found
        ],
        "must_not_contain": [
            r"(他|她|对方)一定是",  # certainty language
            r"(他|她|对方)肯定",  # certainty language
            r"(回避型|焦虑型).*(人格|依恋).*(障碍|诊断)",  # clinical diagnosis
            r"PUA|情感勒索|诱导嫉妒|冷暴力",  # manipulation
        ],
    },
    "cli_export": {
        "must_contain": [
            r"E\d{3}",  # evidence ID reference
            r"S\d{3}",  # session ID reference
            r"置信度|confidence",  # confidence level
        ],
        "must_not_contain": [
            r"(他|她|对方)一定是",  # certainty language
            r"(他|她|对方)肯定",  # certainty language
            r"需要.*更?多.*原始",  # requesting more raw data
        ],
    },
}


def check_output(text: str, scenario: str) -> tuple[list[str], list[str]]:
    """Check output text against scenario requirements.

    Returns:
        (missing_must_contain, found_must_not_contain)
    """
    reqs = SCENARIOS[scenario]
    missing = []
    forbidden_found = []

    for pattern in reqs["must_contain"]:
        if not re.search(pattern, text):
            missing.append(pattern)

    for pattern in reqs["must_not_contain"]:
        if re.search(pattern, text):
            forbidden_found.append(pattern)

    return missing, forbidden_found


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Skill output structure")
    parser.add_argument("--scenario", required=True, choices=SCENARIOS.keys())
    parser.add_argument("file", help="Output file to check")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"File not found: {path}")
        return 1

    text = path.read_text(encoding="utf-8")
    missing, forbidden = check_output(text, args.scenario)

    ok = True
    if missing:
        print(f"Missing required elements ({args.scenario}):")
        for p in missing:
            print(f"  - pattern not found: {p}")
        ok = False

    if forbidden:
        print(f"Forbidden elements found ({args.scenario}):")
        for p in forbidden:
            print(f"  - forbidden pattern: {p}")
        ok = False

    if ok:
        print(f"[PASS] {args.scenario} scenario requirements met")
    else:
        print(f"\n[FAIL] {args.scenario} scenario check failed")

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
