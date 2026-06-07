"""
BondLens 关系信号可靠性审计。

检查项：
1. relationship_signal_ledger.jsonl 中 T1 信号是否被主报告引用。
2. T4 证据是否被用于覆盖或单独支撑关系强结论。
3. 报告是否包含单因子断言或二元化判断。
4. 人格画像/依恋段落是否包含反证和替代解释。
5. 用户纠正中的 evidence_id 是否进入台账和报告。

用法：
    python scripts/relationship_signal_audit.py [analyses_dir]
    python scripts/relationship_signal_audit.py --ledger path --report path
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ANALYSES_DIR = Path(__file__).resolve().parents[1] / "analyses" / "zy-tf"

EVIDENCE_RE = re.compile(r"E-\d{8}-\d{3}")
RELATIONSHIP_KEYWORDS = [
    "喜欢",
    "不喜欢",
    "接受",
    "拒绝",
    "表白",
    "在一起",
    "关系",
    "推进",
    "放弃",
    "回避",
    "依恋",
]
SINGLE_FACTOR_PATTERNS = [
    "就是不喜欢",
    "只是没那么喜欢",
    "就是回避型",
    "完全没可能",
    "完全不可能",
    "完全不喜欢",
    "只是在找借口",
    "唯一解释",
    "只有一种解释",
]
PERSONA_SECTION_MARKERS = ["人格画像", "依恋信号", "依恋假设"]
CORRECTION_FILENAMES = ["user_corrections.jsonl", "corrections.jsonl"]


@dataclass
class AuditIssue:
    code: str
    message: str
    severity: str = "error"


def load_jsonl(path: Path) -> list[dict]:
    """Load a JSONL file. Empty or missing files return an empty list."""
    if not path.exists():
        return []
    records = []
    with path.open(encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                records.append({
                    "_audit_error": f"{path.name}:{lineno}: JSON decode error: {exc}",
                })
    return records


def evidence_ids(text: str) -> set[str]:
    """Return all evidence IDs in text."""
    return set(EVIDENCE_RE.findall(text))


def normalize_tier(value: object) -> str:
    """Normalize a signal tier to uppercase T1/T2/T3/T4."""
    return str(value or "").strip().upper()


def record_evidence_id(record: dict) -> str:
    """Return the evidence ID from a ledger/correction record."""
    return str(record.get("evidence_id") or record.get("id") or "").strip()


def split_heading_blocks(text: str) -> list[str]:
    """Split markdown into heading blocks while preserving heading text."""
    blocks = re.split(r"(?=^#{2,4} )", text, flags=re.MULTILINE)
    return [b.strip() for b in blocks if b.strip()]


def has_relationship_keyword(text: str) -> bool:
    """Check if a block appears to make a relationship-state claim."""
    return any(keyword in text for keyword in RELATIONSHIP_KEYWORDS)


def has_field(text: str, field: str) -> bool:
    """Check for bold markdown fields with either colon style."""
    return f"**{field}**:" in text or f"**{field}**：" in text


def audit_ledger_schema(ledger: list[dict]) -> list[AuditIssue]:
    """Validate minimum ledger fields for deterministic auditability."""
    issues: list[AuditIssue] = []
    required = [
        "evidence_id",
        "date",
        "speaker",
        "tier",
        "signal_type",
        "quote",
        "local_context",
        "later_followup",
        "interpretation_candidates",
    ]
    for idx, record in enumerate(ledger, 1):
        if "_audit_error" in record:
            issues.append(AuditIssue("LEDGER_JSON", record["_audit_error"]))
            continue
        eid = record_evidence_id(record) or f"record-{idx}"
        for field in required:
            if field not in record or record[field] in (None, "", []):
                issues.append(AuditIssue("LEDGER_FIELD", f"{eid} missing required field: {field}"))
        tier = normalize_tier(record.get("tier"))
        if tier not in {"T1", "T2", "T3", "T4"}:
            issues.append(AuditIssue("LEDGER_TIER", f"{eid} has invalid tier: {record.get('tier')}"))
    return issues


def audit_t1_coverage(ledger: list[dict], report_text: str) -> list[AuditIssue]:
    """Ensure all T1 ledger evidence appears in the report."""
    issues: list[AuditIssue] = []
    report_ids = evidence_ids(report_text)
    for record in ledger:
        if normalize_tier(record.get("tier")) != "T1":
            continue
        eid = record_evidence_id(record)
        if eid and eid not in report_ids:
            issues.append(AuditIssue("T1_MISSING", f"T1 signal {eid} is in ledger but missing from report"))
    return issues


def audit_t4_overreach(ledger: list[dict], report_text: str) -> list[AuditIssue]:
    """Flag relationship-claim blocks that cite T4 without T1/T2 support."""
    tier_by_id = {
        record_evidence_id(record): normalize_tier(record.get("tier"))
        for record in ledger
        if record_evidence_id(record)
    }
    issues: list[AuditIssue] = []
    for block in split_heading_blocks(report_text):
        block_ids = evidence_ids(block)
        if not block_ids or not has_relationship_keyword(block):
            continue
        tiers = {tier_by_id.get(eid, "") for eid in block_ids}
        if "T4" in tiers and not ({"T1", "T2"} & tiers):
            preview = " ".join(block.split())[:120]
            issues.append(AuditIssue("T4_OVERREACH", f"T4-only relationship claim: {preview}"))
    return issues


def audit_single_factor_assertions(report_text: str) -> list[AuditIssue]:
    """Scan for single-factor or binary overclaims."""
    issues: list[AuditIssue] = []
    for pattern in SINGLE_FACTOR_PATTERNS:
        if pattern in report_text:
            issues.append(AuditIssue("SINGLE_FACTOR", f"Report contains banned assertion: {pattern}"))
    return issues


def audit_persona_blocks(report_text: str) -> list[AuditIssue]:
    """Check persona/attachment blocks for counterevidence and alternatives."""
    issues: list[AuditIssue] = []
    for block in split_heading_blocks(report_text):
        if not any(marker in block[:160] for marker in PERSONA_SECTION_MARKERS):
            continue
        if "E-" not in block:
            continue
        missing = []
        if not has_field(block, "反证"):
            missing.append("反证")
        if not has_field(block, "替代解释"):
            missing.append("替代解释")
        if missing:
            title = block.splitlines()[0].strip("# ").strip()
            issues.append(AuditIssue("PERSONA_FIELDS", f"{title} missing: {', '.join(missing)}"))
    return issues


def load_correction_ids(paths: Iterable[Path]) -> set[str]:
    """Load evidence IDs referenced by correction files."""
    ids: set[str] = set()
    for path in paths:
        for record in load_jsonl(path):
            eid = record_evidence_id(record)
            if eid:
                ids.add(eid)
            for nested in record.get("evidence_ids", []) or []:
                ids.add(str(nested))
    return ids


def audit_correction_coverage(
    ledger: list[dict], report_text: str, correction_paths: Iterable[Path]
) -> list[AuditIssue]:
    """Ensure user-correction evidence IDs appear in both ledger and report."""
    correction_ids = load_correction_ids(correction_paths)
    if not correction_ids:
        return []
    ledger_ids = {record_evidence_id(record) for record in ledger}
    report_ids = evidence_ids(report_text)
    issues: list[AuditIssue] = []
    for eid in sorted(correction_ids):
        if eid not in ledger_ids:
            issues.append(AuditIssue("CORRECTION_LEDGER", f"Correction evidence {eid} missing from ledger"))
        if eid not in report_ids:
            issues.append(AuditIssue("CORRECTION_REPORT", f"Correction evidence {eid} missing from report"))
    return issues


def audit_paths(
    ledger_path: Path,
    report_path: Path,
    correction_paths: Iterable[Path] = (),
) -> list[AuditIssue]:
    """Run all relationship-signal reliability checks."""
    issues: list[AuditIssue] = []
    if not ledger_path.exists():
        return [AuditIssue("LEDGER_MISSING", f"Missing relationship signal ledger: {ledger_path}")]
    if not report_path.exists():
        return [AuditIssue("REPORT_MISSING", f"Missing report: {report_path}")]

    ledger = load_jsonl(ledger_path)
    report_text = report_path.read_text(encoding="utf-8")
    issues.extend(audit_ledger_schema(ledger))
    issues.extend(audit_t1_coverage(ledger, report_text))
    issues.extend(audit_t4_overreach(ledger, report_text))
    issues.extend(audit_single_factor_assertions(report_text))
    issues.extend(audit_persona_blocks(report_text))
    issues.extend(audit_correction_coverage(ledger, report_text, correction_paths))
    return issues


def default_report_path(analyses_dir: Path) -> Path:
    """Choose the main BondLens report in an analysis directory."""
    candidates = sorted(analyses_dir.glob("bondlens_report*.md"))
    if candidates:
        return candidates[0]
    return analyses_dir / "bondlens_report.md"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit BondLens relationship signal reliability.")
    parser.add_argument("analyses_dir", nargs="?", default=str(ANALYSES_DIR))
    parser.add_argument("--ledger", type=Path, default=None)
    parser.add_argument("--report", type=Path, default=None)
    parser.add_argument("--corrections", type=Path, nargs="*", default=None)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    analyses_dir = Path(args.analyses_dir)
    ledger_path = args.ledger or analyses_dir / "relationship_signal_ledger.jsonl"
    report_path = args.report or default_report_path(analyses_dir)
    correction_paths = args.corrections
    if correction_paths is None:
        correction_paths = [analyses_dir / name for name in CORRECTION_FILENAMES]

    print("=" * 60)
    print("BondLens Relationship Signal Audit")
    print("=" * 60)
    print(f"Ledger: {ledger_path}")
    print(f"Report: {report_path}")

    issues = audit_paths(ledger_path, report_path, correction_paths)
    if issues:
        print(f"\n[FAIL] {len(issues)} issue(s)")
        for issue in issues:
            print(f"  [{issue.severity.upper()}] {issue.code}: {issue.message}")
        return 1

    print("\n[PASS] Relationship signal reliability checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
