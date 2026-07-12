"""Single-source relationship analysis and deterministic Markdown/HTML renderers."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

from ..schema import RelationshipSignalCandidate, RelationshipSignalLedgerEntry


def _event_view(item: RelationshipSignalLedgerEntry) -> dict[str, Any]:
    return {
        "event_id": item.event_id,
        "type": item.candidate_type,
        "quote": item.quote,
        "response": item.response_summary,
        "conditions": item.conditions,
        "time_anchor": item.time_anchor,
        "consensus_state": item.consensus_state,
        "boundary_effect": item.boundary_effect,
        "decision": item.decision,
        "tier": item.tier,
        "reason": item.decision_reason,
        "counterevidence_ids": item.counterevidence_ids,
        "must_not_infer": item.must_not_infer,
        "created_at": item.created_at.isoformat(),
    }


def build_relationship_analysis(
    *,
    ledger: list[RelationshipSignalLedgerEntry] | None = None,
    candidates: list[RelationshipSignalCandidate] | None = None,
    interaction_stats: dict | None = None,
    mode: str = "quick",
) -> dict[str, Any]:
    """Build the sole factual source used by every report format."""
    ledger = ledger or []
    candidates = candidates or []
    included = [item for item in ledger if item.tier is not None]
    t1 = [item for item in included if item.tier == "T1"]
    events = [_event_view(item) for item in t1]
    pending = not ledger and bool(candidates)

    has_rejection = any(
        "explicit_rejection" in item.candidate_type or item.boundary_effect == "stop_progression"
        for item in t1
    )
    has_boundary = any(item.boundary_effect not in {"", "none"} for item in t1)
    divergent = any(item.consensus_state == "divergent" for item in t1)
    conditional = any("conditional_acceptance" in item.candidate_type for item in t1)

    if pending:
        action = "先完成候选事件的语义审核；在此之前不输出关系结论。"
        avoid = ["不要把候选置信度当作关系结论", "不要用日常热度覆盖待审核的边界表达"]
        draft = ""
    elif has_rejection:
        action = "按明确拒绝或暂停执行降压，不再从日常聊天中反推隐藏好感。"
        avoid = ["不要继续推进关系", "不要用高互动统计否定对方原话"]
        draft = "我听明白了，会尊重你的决定和边界，不再给你压力。"
    elif has_boundary:
        action = "先遵守已经表达的联系、空间或同意边界，再观察是否由对方主动重启讨论。"
        avoid = ["不要绕过边界测试对方", "不要连续追问关系答案"]
        draft = "收到，我会按你说的给彼此空间。需要沟通时你可以告诉我。"
    elif divergent:
        action = "双方关系定义不一致，优先做一次低压力澄清，而不是直接推进。"
        avoid = ["不要默认双方已经达成关系共识"]
        draft = "我想确认我们对现在这段关系的理解是否一致，你可以按真实想法说。"
    elif conditional:
        action = "保留开放条件，也保留现实限制；只核对条件责任与时间点，不催兑现。"
        avoid = ["不要把条件性接受压成已经接受", "不要把它压成永久拒绝"]
        draft = "我理解现在还不是开始关系的时点。条件或想法有变化时，我们再清楚地谈一次。"
    elif not t1:
        action = "目前没有经确认的关系讨论；若需要判断关系性质，应直接、低压力地澄清。"
        avoid = ["不要仅凭回复速度、消息长度或聊天频率判断喜欢"]
        draft = "我想确认一下，你怎么看我们现在的关系？不用照顾我的期待，真实说就好。"
    else:
        action = "按双方已经明确说过的共识行动，并为未决条件设置一次低压力复核。"
        avoid = ["不要把假设写成事实"]
        draft = ""

    aligned = [item for item in events if item["consensus_state"] == "aligned"]
    disagreements = [
        item for item in events if item["consensus_state"] in {"divergent", "open", "unanswered"}
    ]
    changes = [
        item for item in events if item["counterevidence_ids"] or "ambivalence" in item["type"]
    ]
    cannot = ["不能判断隐藏好感、临床人格或未来必然结果"]
    if pending:
        cannot.append("候选尚未完成语义审核，不能生成正式关系判断")
    if not events:
        cannot.append("关系性质不足以判断")

    return {
        "schema_version": "0.12.0",
        "mode": mode,
        "review_status": "pending_semantic_review" if pending else "finalized",
        "critical_relationship_discussions": events,
        "consensus": aligned,
        "disagreements_and_open_conditions": disagreements,
        "recent_reversals_or_phase_changes": changes,
        "judgment_scope": {
            "can_judge": ["明确说过的关系定义、条件、边界及其后续变化"] if events else [],
            "cannot_judge": cannot,
        },
        "action_brief": {
            "this_week": action,
            "avoid": avoid,
            "message_draft": draft,
            "boundary_checked": not has_boundary or draft != "",
        },
        "profiles_and_hypotheses": {
            "status": "evidence_required",
            "rule": "稳定特征、压力状态、关系特定行为和自我陈述必须分开；不得覆盖 T1。",
        },
        "uncertainty_and_counterevidence": {
            "event_count": len(events),
            "excluded_count": sum(item.decision == "excluded" for item in ledger),
            "pending_candidate_count": len(candidates) if pending else 0,
            "counterevidence_ids": list(
                dict.fromkeys(value for item in events for value in item["counterevidence_ids"])
            ),
        },
        "interaction_stats": interaction_stats or {},
    }


def write_relationship_analysis(path: Path, analysis: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(analysis, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def render_analysis_markdown(analysis: dict[str, Any]) -> str:
    lines = ["# LakeSkill 湖镜关系分析", "", f"> 审核状态：{analysis['review_status']}", ""]
    sections = [
        ("关键关系讨论", analysis["critical_relationship_discussions"]),
        ("已有共识", analysis["consensus"]),
        ("分歧与开放条件", analysis["disagreements_and_open_conditions"]),
        ("最近改口或阶段变化", analysis["recent_reversals_or_phase_changes"]),
    ]
    for title, items in sections:
        lines.extend([f"## {title}", ""])
        if not items:
            lines.append("- 未确认")
        for item in items:
            lines.append(f"- **{item['event_id']}**：{item['quote']}")
            lines.append(f"  - 状态：{item['consensus_state']}；条件：{', '.join(item['conditions']) or '无'}")
        lines.append("")
    scope = analysis["judgment_scope"]
    lines.extend(["## 能判断与不能判断", ""])
    lines.extend(f"- 能判断：{item}" for item in scope["can_judge"])
    lines.extend(f"- 不能判断：{item}" for item in scope["cannot_judge"])
    brief = analysis["action_brief"]
    lines.extend(["", "## 一分钟行动卡", "", f"- 本周：{brief['this_week']}"])
    lines.extend(f"- 避免：{item}" for item in brief["avoid"])
    if brief["message_draft"]:
        lines.append(f"- 可发送：{brief['message_draft']}")
    lines.extend(["", "## 双方画像、互动模式和依恋假设", ""])
    lines.append(f"- {analysis['profiles_and_hypotheses']['rule']}")
    lines.extend(["", "## 不确定性与反证", ""])
    lines.append(f"- 反证 ID：{', '.join(analysis['uncertainty_and_counterevidence']['counterevidence_ids']) or '未记录'}")
    lines.append("- 互动统计仅作为 T4 描述背景，不生成爱情总分。")
    return "\n".join(lines) + "\n"


def render_analysis_html(analysis: dict[str, Any]) -> str:
    def esc(value: Any) -> str:
        return html.escape(str(value))

    events = analysis["critical_relationship_discussions"]
    event_html = "".join(
        "<details><summary><b>" + esc(item["event_id"]) + "</b> · " + esc(item["type"]) +
        "</summary><blockquote>" + esc(item["quote"]) + "</blockquote><p>" +
        esc(item["response"]) + "</p><p class='meta'>共识 " + esc(item["consensus_state"]) +
        " · 条件 " + esc("、".join(item["conditions"]) or "未明确") + "</p></details>"
        for item in events
    ) or "<p class='empty'>没有经确认的 T1 关系讨论，关系性质不足以判断。</p>"
    brief = analysis["action_brief"]
    avoid = "".join("<li>" + esc(item) + "</li>" for item in brief["avoid"])
    scope = "".join("<li>" + esc(item) + "</li>" for item in analysis["judgment_scope"]["cannot_judge"])
    stats = analysis.get("interaction_stats") or {}
    coverage = stats.get("coverage", {})
    return f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>LakeSkill 湖镜关系分析</title><style>
:root{{--ink:#142422;--muted:#64716f;--paper:#f4f0e7;--lake:#147d73;--line:#c8d1cc}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font-family:"Noto Serif SC","Songti SC",serif;line-height:1.75}}
header{{min-height:56vh;padding:9vw 8vw 6vw;background:var(--ink);color:#fff;display:flex;flex-direction:column;justify-content:end}}
.brand{{letter-spacing:.18em;color:#87d4c8;font:600 13px system-ui}}h1{{font-size:clamp(42px,8vw,108px);line-height:.95;margin:.22em 0;max-width:10ch}}
.lead{{max-width:52ch;color:#d7e0dc;font-family:system-ui}}main{{max-width:1040px;margin:auto;padding:7vw 6vw}}section{{padding:4rem 0;border-bottom:1px solid var(--line)}}
h2{{font-size:clamp(25px,4vw,46px);margin:0 0 1.4rem}}.brief{{font-size:clamp(22px,3vw,34px);max-width:26ch}}
.meta,.empty{{color:var(--muted)}}details{{padding:1.2rem 0;border-top:1px solid var(--line)}}summary{{cursor:pointer;font-family:system-ui}}
blockquote{{font-size:1.25rem;margin:1.2rem 0;padding-left:1.2rem;border-left:3px solid var(--lake)}}code{{font-family:ui-monospace}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:4rem}}@media(max-width:700px){{.grid{{grid-template-columns:1fr}}header{{min-height:68vh}}}}
@media(prefers-reduced-motion:no-preference){{header>*{{animation:rise .7s both}}header>*:nth-child(2){{animation-delay:.08s}}header>*:nth-child(3){{animation-delay:.16s}}details{{transition:background .2s}}details:hover{{background:#ebe7dc}}@keyframes rise{{from{{opacity:0;transform:translateY(18px)}}}}}}
</style></head><body>
<header><div class="brand">LAKESKILL · 湖镜</div><h1>先找全原话，再决定下一步。</h1><p class="lead">审核状态：{esc(analysis["review_status"])}。不读心，不把边界解释成隐藏好感。</p></header>
<main><section><div class="brand">一分钟行动卡</div><h2>现在最重要的事</h2><p class="brief">{esc(brief["this_week"])}</p><ul>{avoid}</ul><p>{esc(brief["message_draft"])}</p></section>
<section><div class="brand">T1 全量保留</div><h2>关键关系讨论</h2>{event_html}</section>
<section class="grid"><div><h2>不能判断</h2><ul>{scope}</ul></div><div><h2>数据覆盖</h2><p>{esc(coverage.get("message_count", 0))} 条消息 · {esc(coverage.get("session_count", 0))} 个 session</p><p class="meta">互动统计仅作 T4，不展示爱情总分。</p></div></section>
</main></body></html>"""
