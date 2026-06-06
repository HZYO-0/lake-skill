"""Data readiness checks for bondlens doctor."""

from datetime import datetime
from typing import Optional

from .schema import Message, Session, SenderRole


def run_doctor_checks(
    messages: list[Message], sessions: Optional[list[Session]] = None
) -> dict:
    """Run all data readiness checks.

    Returns dict with:
      - checks: list of {name, passed, summary, detail}
      - overall: "ready" | "marginal" | "insufficient"
    """
    checks = [
        check_message_count(messages),
        check_date_range(messages),
        check_both_side_balance(messages),
        check_scene_coverage(messages, sessions),
        check_privacy_risk(messages),
    ]

    failed = sum(1 for c in checks if not c["passed"])
    if failed == 0:
        overall = "ready"
    elif failed <= 2:
        overall = "marginal"
    else:
        overall = "insufficient"

    return {"checks": checks, "overall": overall}


def check_message_count(messages: list[Message]) -> dict:
    """Check if message count meets thresholds."""
    count = len(messages)
    if count >= 100:
        return {"name": "消息量", "passed": True, "summary": f"{count} 条（充分）", "detail": "≥100 条，可进行完整分析"}
    elif count >= 30:
        return {"name": "消息量", "passed": False, "summary": f"{count} 条（基本）", "detail": "30-99 条，分析将标注低置信度"}
    else:
        return {"name": "消息量", "passed": False, "summary": f"{count} 条（不足）", "detail": "<30 条，仅能输出局部观察"}


def check_date_range(messages: list[Message]) -> dict:
    """Check if date range meets thresholds."""
    if not messages:
        return {"name": "时间跨度", "passed": False, "summary": "无消息", "detail": "无法计算时间跨度"}

    timestamps = [m.timestamp for m in messages if m.timestamp]
    if len(timestamps) < 2:
        return {"name": "时间跨度", "passed": False, "summary": "不足 1 天", "detail": "仅 1 条消息，无法分析趋势"}

    min_ts = min(timestamps)
    max_ts = max(timestamps)
    days = (max_ts - min_ts).days

    if days >= 7:
        return {"name": "时间跨度", "passed": True, "summary": f"{days} 天（充分）", "detail": "≥7 天，可分析趋势"}
    elif days >= 1:
        return {"name": "时间跨度", "passed": False, "summary": f"{days} 天（基本）", "detail": "1-6 天，仅能分析短期模式"}
    else:
        return {"name": "时间跨度", "passed": False, "summary": "< 1 天", "detail": "单场景快照，无法分析趋势"}


def check_both_side_balance(messages: list[Message]) -> dict:
    """Check if both sides participate in conversation."""
    if not messages:
        return {"name": "双方平衡", "passed": False, "summary": "无消息", "detail": "无法计算参与度"}

    self_count = sum(1 for m in messages if m.sender_role == SenderRole.SELF)
    target_count = sum(1 for m in messages if m.sender_role == SenderRole.TARGET)
    total = self_count + target_count

    if total == 0:
        return {"name": "双方平衡", "passed": False, "summary": "无有效消息", "detail": "无法识别发送者"}

    self_pct = self_count / total * 100
    target_pct = target_count / total * 100

    if 30 <= self_pct <= 70 and 30 <= target_pct <= 70:
        return {"name": "双方平衡", "passed": True, "summary": f"我 {self_pct:.0f}% / 对方 {target_pct:.0f}%", "detail": "双方参与基本均衡"}
    elif 20 <= self_pct <= 80 and 20 <= target_pct <= 80:
        return {"name": "双方平衡", "passed": False, "summary": f"我 {self_pct:.0f}% / 对方 {target_pct:.0f}%", "detail": "参与度有偏差，分析时需注意"}
    else:
        return {"name": "双方平衡", "passed": False, "summary": f"我 {self_pct:.0f}% / 对方 {target_pct:.0f}%", "detail": "严重不平衡，可能无法分析互动模式"}


def check_scene_coverage(
    messages: list[Message], sessions: Optional[list[Session]] = None
) -> dict:
    """Check if conversation covers multiple scene types."""
    if sessions is None:
        return {"name": "场景覆盖", "passed": False, "summary": "未提供 sessions", "detail": "无法评估场景多样性，建议先运行 segment"}

    episode_types: set[str] = set()
    for s in sessions:
        for ep in s.episode_type:
            episode_types.add(ep)

    count = len(episode_types)
    if count >= 3:
        return {"name": "场景覆盖", "passed": True, "summary": f"{count} 种场景", "detail": f"场景类型: {', '.join(sorted(episode_types))}"}
    elif count >= 1:
        return {"name": "场景覆盖", "passed": False, "summary": f"{count} 种场景", "detail": f"场景类型: {', '.join(sorted(episode_types))}，建议补充更多场景"}
    else:
        return {"name": "场景覆盖", "passed": False, "summary": "0 种场景", "detail": "未检测到场景类型，可能需要更长时间跨度的数据"}


def check_privacy_risk(messages: list[Message]) -> dict:
    """Check if messages have been redacted."""
    if not messages:
        return {"name": "隐私风险", "passed": False, "summary": "无消息", "detail": "无法评估"}

    has_redacted = sum(1 for m in messages if m.text_redacted)
    total = len(messages)

    if has_redacted == total:
        return {"name": "隐私风险", "passed": True, "summary": "已全部脱敏", "detail": "所有消息已脱敏处理"}
    elif has_redacted > 0:
        return {"name": "隐私风险", "passed": False, "summary": f"{has_redacted}/{total} 已脱敏", "detail": "部分消息未脱敏，上传前请运行 redact"}
    else:
        return {"name": "隐私风险", "passed": False, "summary": "未脱敏", "detail": "消息未脱敏，上传前请运行 bondlens redact"}


def format_readiness_report(results: dict) -> str:
    """Format doctor check results as markdown."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    overall = results["overall"]

    verdict = {"ready": "✅ 数据充分，可进行完整分析", "marginal": "⚠️ 数据基本可用，部分维度可能置信度较低", "insufficient": "❌ 数据不足，建议补充更多聊天记录"}

    lines = [
        "# BondLens Data Readiness Report",
        "",
        f"**Generated**: {now}",
        f"**Overall**: {verdict.get(overall, overall)}",
        "",
        "## Checks",
        "",
        "| 检查项 | 状态 | 说明 |",
        "|--------|------|------|",
    ]

    for check in results["checks"]:
        status = "✅ OK" if check["passed"] else "⚠️ WARN"
        lines.append(f"| {check['name']} | {status} | {check['detail']} |")

    lines.extend([
        "",
        "## Recommendation",
        "",
    ])

    if overall == "ready":
        lines.append("数据充分，建议运行完整 BondLens 分析流程。")
    elif overall == "marginal":
        lines.append("数据基本可用。建议先运行分析，同时标注低置信度维度。如有条件，补充更多时间段的聊天记录。")
    else:
        lines.append("数据不足。建议：")
        lines.append("- 补充更多聊天记录（目标 100+ 条）")
        lines.append("- 确保覆盖至少 7 天的时间跨度")
        lines.append("- 确保双方都有参与对话")

    return "\n".join(lines)
