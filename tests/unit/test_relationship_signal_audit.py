"""Regression tests for BondLens relationship signal reliability audit."""

import importlib.util
import json
import sys
import uuid
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_ROOT = PROJECT_ROOT / "work" / "test-artifacts" / "relationship_signal_audit"
AUDIT_MODULE_PATH = PROJECT_ROOT / "scripts" / "relationship_signal_audit.py"

_audit_spec = importlib.util.spec_from_file_location(
    "bondlens_relationship_signal_audit", AUDIT_MODULE_PATH
)
assert _audit_spec is not None
assert _audit_spec.loader is not None
_audit_module = importlib.util.module_from_spec(_audit_spec)
sys.modules[_audit_spec.name] = _audit_module
_audit_spec.loader.exec_module(_audit_module)
audit_paths = _audit_module.audit_paths


def _case_dir(name: str) -> Path:
    path = ARTIFACT_ROOT / f"{name}-{uuid.uuid4().hex}"
    path.mkdir(parents=True, exist_ok=False)
    return path


def _write_jsonl(path: Path, records: list[dict]) -> None:
    path.write_text(
        "\n".join(json.dumps(record, ensure_ascii=False) for record in records) + "\n",
        encoding="utf-8",
    )


def _base_record(evidence_id: str, tier: str, signal_type: str, quote: str) -> dict:
    return {
        "evidence_id": evidence_id,
        "date": "2026-05-17",
        "speaker": "target",
        "tier": tier,
        "signal_type": signal_type,
        "quote": quote,
        "local_context": "关系定义对话",
        "later_followup": "后续仍有日常互动",
        "interpretation_candidates": ["开放条件", "委婉暂停"],
        "counterevidence_ids": [],
        "source": "chat_record",
        "confidence": "medium",
    }


def test_audit_passes_for_multifactor_report():
    """A report that cites T1 and includes counterevidence passes."""
    tmp_path = _case_dir("pass")
    ledger = tmp_path / "relationship_signal_ledger.jsonl"
    report = tmp_path / "bondlens_report.md"

    _write_jsonl(
        ledger,
        [
            _base_record("E-20260517-001", "T1", "conditional_acceptance", "如果想法明确了，那就 ok"),
            _base_record("E-20260518-001", "T2", "repair", "我们慢慢来"),
            _base_record("E-20260519-001", "T4", "daily_context", "今天吃什么"),
        ],
    )
    report.write_text(
        """
# BondLens 关系分析报告

## Layer 1.5: 关系信号台账摘要
T1 条件性时间线：E-20260517-001。T2 修复信号：E-20260518-001。

## Layer 2: 对方 人格画像
### 关系压力下的退缩信号
**观察**: 对方在关系定义后给出开放条件。
**证据**: E-20260517-001, E-20260518-001
**推断**: 感情、现实顾虑和自我保护可能同时存在。
**置信度**: 中
**反证**: E-20260518-001 仍有修复行为。
**替代解释**: 也可能只是现实安排未定。

## Reliability Audit
**关系信号台账**: PASS
""",
        encoding="utf-8",
    )

    assert audit_paths(ledger, report) == []


def test_audit_flags_missing_t1_and_single_factor_assertion():
    """Missing T1 coverage and binary overclaim are audit failures."""
    tmp_path = _case_dir("missing-t1")
    ledger = tmp_path / "relationship_signal_ledger.jsonl"
    report = tmp_path / "bondlens_report.md"

    _write_jsonl(
        ledger,
        [
            _base_record("E-20260517-001", "T1", "conditional_acceptance", "如果想法明确了，那就 ok"),
            _base_record("E-20260519-001", "T4", "daily_context", "每天聊天很多"),
        ],
    )
    report.write_text(
        """
# BondLens 关系分析报告

## Layer -1: 关系行动卡
你们每天聊天很多（E-20260519-001），她就是不喜欢你。
""",
        encoding="utf-8",
    )

    issues = audit_paths(ledger, report)
    codes = {issue.code for issue in issues}
    assert "T1_MISSING" in codes
    assert "T4_OVERREACH" in codes
    assert "SINGLE_FACTOR" in codes


def test_audit_requires_persona_counterevidence_and_alternatives():
    """Persona/attachment evidence blocks must include counterevidence and alternatives."""
    tmp_path = _case_dir("persona-fields")
    ledger = tmp_path / "relationship_signal_ledger.jsonl"
    report = tmp_path / "bondlens_report.md"

    _write_jsonl(
        ledger,
        [_base_record("E-20260604-001", "T1", "self_understanding", "我是回避型")],
    )
    report.write_text(
        """
# BondLens 关系分析报告

## Layer 2: 对方 人格画像
### 依恋信号
**观察**: 对方说自己是回避型。
**证据**: E-20260604-001
**推断**: 这是自我陈述，不是诊断。
**置信度**: 中
""",
        encoding="utf-8",
    )

    issues = audit_paths(ledger, report)
    assert "PERSONA_FIELDS" in {issue.code for issue in issues}


def test_audit_requires_user_correction_coverage():
    """User correction evidence must appear in both ledger and report."""
    tmp_path = _case_dir("correction")
    ledger = tmp_path / "relationship_signal_ledger.jsonl"
    report = tmp_path / "bondlens_report.md"
    corrections = tmp_path / "corrections.jsonl"

    _write_jsonl(
        ledger,
        [_base_record("E-20260517-001", "T1", "conditional_acceptance", "如果想法明确了，那就 ok")],
    )
    _write_jsonl(
        corrections,
        [{"evidence_id": "E-20260418-001", "corrected": "对方自称回避型"}],
    )
    report.write_text(
        """
# BondLens 关系分析报告
E-20260517-001 已进入关系信号台账。
""",
        encoding="utf-8",
    )

    issues = audit_paths(ledger, report, [corrections])
    codes = {issue.code for issue in issues}
    assert "CORRECTION_LEDGER" in codes
    assert "CORRECTION_REPORT" in codes
