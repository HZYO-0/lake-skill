"""High-recall extraction and auditable review of relationship discussions."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path

from .jsonl_utils import write_jsonl_models
from .schema import (
    Evidence,
    Message,
    RelationshipSignalCandidate,
    RelationshipSignalDecision,
    RelationshipSignalLedgerEntry,
    Session,
)


@dataclass(frozen=True)
class SignalRule:
    name: str
    pattern: re.Pattern[str]
    polarity: str
    base_confidence: float


RULES = (
    SignalRule(
        "conditional_acceptance",
        re.compile(r"(?:\u7b49|\u7b49\u5230|\u4ee5\u540e|\u5c06\u6765|\u8fc7\u6bb5\u65f6\u95f4|\u5de5\u4f5c\u7a33\u5b9a|\u6bd5\u4e1a|\u51c6\u5907\u597d).{0,12}(?:\u518d\u8bf4|\u518d\u770b|\u518d\u8003\u8651|\u5f00\u59cb|\u5728\u4e00\u8d77)|(?:\u4e0d\u662f\u4e0d\u559c\u6b22|\u6709\u597d\u611f).{0,16}(?:\u53ea\u662f|\u4f46\u662f|\u4f46).{0,16}(?:\u73b0\u5728|\u6682\u65f6|\u4e0d\u60f3|\u4e0d\u80fd|\u6ca1\u529e\u6cd5)"),
        "mixed",
        0.92,
    ),
    SignalRule(
        "relationship_definition",
        re.compile(r"(?:\u6211\u4eec|\u54b1\u4eec).{0,8}(?:\u662f\u4ec0\u4e48\u5173\u7cfb|\u7b97\u4ec0\u4e48|\u662f\u670b\u53cb|\u505a\u670b\u53cb|\u5148\u505a\u670b\u53cb|\u662f\u5bf9\u8c61|\u7537\u5973\u670b\u53cb|\u5728\u4e00\u8d77)|(?:\u53ea\u662f|\u5c31\u662f|\u5f53).{0,4}(?:\u670b\u53cb|\u5bf9\u8c61|\u7537\u5973\u670b\u53cb)"),
        "neutral",
        0.93,
    ),
    SignalRule(
        "confession_or_progression",
        re.compile(r"(?:\u6211|\u8fd8\u662f|\u771f\u7684).{0,5}(?:\u559c\u6b22\u4f60|\u7231\u4f60|\u5bf9\u4f60\u6709\u597d\u611f)|(?:\u60f3|\u613f\u610f|\u8981\u4e0d\u8981).{0,8}(?:\u548c\u4f60\u5728\u4e00\u8d77|\u505a\u4f60\u5bf9\u8c61|\u8c08\u604b\u7231|\u8bd5\u4e00\u8bd5)"),
        "positive",
        0.91,
    ),
    SignalRule(
        "explicit_rejection",
        re.compile(r"(?<!\u4e0d\u662f)(?:\u6211)?(?:\u4e0d\u559c\u6b22\u4f60|\u4e0d\u7231\u4f60|\u4e0d\u60f3\u548c\u4f60\u5728\u4e00\u8d77|\u4e0d\u53ef\u80fd\u5728\u4e00\u8d77|\u6ca1\u611f\u89c9|\u522b\u7b49\u6211|\u4e0d\u8981\u8ffd\u6211|\u63a5\u53d7\u4e0d\u4e86\u4f60)"),
        "negative",
        0.95,
    ),
    SignalRule(
        "pause_or_downgrade",
        re.compile(r"(?:\u73b0\u5728|\u6682\u65f6|\u6700\u8fd1).{0,8}(?:\u4e0d\u60f3|\u4e0d\u80fd|\u6ca1\u529e\u6cd5|\u4e0d\u9002\u5408).{0,8}(?:\u5f00\u59cb|\u8c08\u604b\u7231|\u5728\u4e00\u8d77|\u786e\u5b9a\u5173\u7cfb)|(?:\u5148|\u8fd8\u662f).{0,4}(?:\u505a\u670b\u53cb|\u5f53\u670b\u53cb)|(?:\u5173\u7cfb|\u8054\u7cfb).{0,6}(?:\u6682\u505c|\u51b7\u9759|\u964d\u6e29)"),
        "negative",
        0.91,
    ),
    SignalRule(
        "boundary_or_consent",
        re.compile(r"(?:\u4e0d\u8981|\u522b).{0,10}(?:\u903c\u6211|\u50ac\u6211|\u95ee\u4e86|\u8054\u7cfb\u6211|\u53d1\u6d88\u606f|\u78b0\u6211)|(?:\u9700\u8981|\u7ed9\u6211).{0,8}(?:\u7a7a\u95f4|\u65f6\u95f4|\u51b7\u9759)|(?:\u8054\u7cfb|\u6d88\u606f).{0,8}(?:\u5c11\u4e00\u70b9|\u9891\u7387|\u592a\u591a|\u592a\u9891\u7e41)|(?:\u6211\u4e0d\u540c\u610f|\u6211\u4e0d\u613f\u610f|\u5c0a\u91cd\u6211\u7684\u8fb9\u754c)"),
        "negative",
        0.91,
    ),
    SignalRule(
        "future_or_commitment",
        re.compile(r"(?:\u6211\u4eec|\u548c\u4f60|\u54b1\u4eec).{0,10}(?:\u4ee5\u540e|\u672a\u6765|\u7ed3\u5a5a|\u5a5a\u59fb|\u89c1\u5bb6\u957f|\u751f\u5b69\u5b50|\u957f\u671f|\u627f\u8bfa|\u4e00\u8d77\u751f\u6d3b)|(?:\u7b49\u6211|\u7b49\u4f60).{0,8}(?:\u6bd5\u4e1a|\u5de5\u4f5c\u7a33\u5b9a|\u51c6\u5907\u597d).{0,8}(?:\u5728\u4e00\u8d77|\u7ed3\u5a5a|\u5f00\u59cb)"),
        "positive",
        0.88,
    ),
    SignalRule(
        "exclusivity_or_third_party",
        re.compile(r"(?:\u6211\u4eec|\u4f60|\u6211).{0,8}(?:\u6392\u4ed6|\u4e13\u4e00|\u5fe0\u8bda|\u51fa\u8f68|\u66a7\u6627\u522b\u4eba|\u7b2c\u4e09\u8005)|(?:\u53ea\u80fd|\u53ea\u60f3).{0,5}(?:\u548c\u4f60|\u8ddf\u4f60|\u559c\u6b22\u4f60)"),
        "neutral",
        0.87,
    ),
    SignalRule(
        "breakup_repair_or_exit",
        re.compile(r"(?:\u6211\u4eec|\u54b1\u4eec).{0,8}(?:\u5206\u624b|\u590d\u5408|\u548c\u597d|\u91cd\u65b0\u5f00\u59cb|\u5230\u6b64\u4e3a\u6b62)|(?:\u4f53\u9762|\u597d\u597d).{0,5}(?:\u7ed3\u675f|\u544a\u522b)|(?:\u518d\u7ed9|\u7ed9\u5f7c\u6b64).{0,8}(?:\u4e00\u6b21\u673a\u4f1a|\u673a\u4f1a)"),
        "mixed",
        0.92,
    ),
    SignalRule(
        "relationship_self_statement",
        re.compile(r"(?:\u6211).{0,8}(?:\u4e0d\u914d|\u6015\u803d\u8bef\u4f60|\u5bb3\u6015\u5173\u7cfb|\u4e0d\u6562\u5f00\u59cb|\u4e0d\u60f3\u604b\u7231|\u56de\u907f\u4eb2\u5bc6|\u4e0d\u503c\u5f97\u88ab\u7231|\u6ca1\u51c6\u5907\u597d)"),
        "neutral",
        0.86,
    ),
    SignalRule(
        "ambivalence_or_reversal",
        re.compile(r"(?:\u6211\u4e5f\u4e0d\u77e5\u9053|\u6211\u4e0d\u786e\u5b9a|\u518d\u770b\u770b|\u4ee5\u540e\u518d\u8bf4|\u5f53\u6211\u6ca1\u8bf4|\u6536\u56de\u521a\u624d|\u4e4b\u524d\u8bf4\u7684.{0,6}(?:\u4e0d\u7b97|\u53d8\u4e86)|\u4e00\u4f1a\u513f.{0,8}\u4e00\u4f1a\u513f)"),
        "mixed",
        0.78,
    ),
)

MEDIA_OR_QUOTE = re.compile(r"(?:\u6b4c\u8bcd|\u6b4c\u91cc|\u7535\u5f71\u91cc|\u5c0f\u8bf4\u91cc|\u53f0\u8bcd|\u8f6c\u53d1|\u5f15\u7528|\u4ed6\u8bf4|\u5979\u8bf4|\u539f\u8bdd\u662f)")
THIRD_PARTY = re.compile(r"(?:\u6211\u670b\u53cb|\u6211\u540c\u4e8b|\u6211\u540c\u5b66|\u6211\u95fa\u871c|\u6211\u5144\u5f1f|\u4ed6\u4eec|\u522b\u4eba).{0,12}(?:\u7ed3\u5a5a|\u5206\u624b|\u590d\u5408|\u8868\u767d|\u604b\u7231|\u5bf9\u8c61|\u7537\u5973\u670b\u53cb)")
DIRECT_RELATION = re.compile(r"(?:\u6211\u4eec|\u54b1\u4eec|\u4f60\u548c\u6211|\u6211\u548c\u4f60|\u5bf9\u4f60|\u559c\u6b22\u4f60|\u548c\u4f60|\u8ddf\u4f60)")
NEGATED_REJECTION = re.compile(r"\u4e0d\u662f\u4e0d\u559c\u6b22\u4f60|\u5e76\u4e0d\u662f\u4e0d\u559c\u6b22\u4f60|\u4e0d\u662f\u6ca1\u6709\u611f\u89c9")
CONDITION = re.compile(r"((?:\u7b49|\u7b49\u5230|\u4ee5\u540e|\u5c06\u6765|\u8fc7\u6bb5\u65f6\u95f4|\u5de5\u4f5c\u7a33\u5b9a|\u6bd5\u4e1a|\u51c6\u5907\u597d).{0,16}(?:\u518d\u8bf4|\u518d\u770b|\u518d\u8003\u8651|\u5f00\u59cb|\u5728\u4e00\u8d77|\u7ed3\u5a5a)?)")
TIME_ANCHOR = re.compile(r"(?:\u73b0\u5728|\u6682\u65f6|\u4ee5\u540e|\u5c06\u6765|\u8fc7\u6bb5\u65f6\u95f4|\u6bd5\u4e1a\u540e|\u5de5\u4f5c\u7a33\u5b9a\u540e|\u4e0b\u5468|\u4e0b\u4e2a\u6708|\u660e\u5e74|\d{1,2}[\u6708\u53f7\u65e5])")


@dataclass
class Hit:
    index: int
    message: Message
    session: Session
    evidence_ids: list[str]
    types: list[str]
    polarity: str
    confidence: float
    review_hint: str | None = None


def _text(message: Message) -> str:
    return (message.text_redacted or message.text or "").strip()


def _quality_factor(message: Message) -> float:
    if message.quality.asr_confidence is not None and message.quality.asr_confidence < 0.75:
        return 0.62
    if message.quality.ocr_confidence is not None and message.quality.ocr_confidence < 0.80:
        return 0.62
    if message.quality.parse_confidence.value == "low":
        return 0.70
    return 1.0


def _detect_hit(
    index: int,
    message: Message,
    session: Session,
    evidence_ids: list[str],
) -> Hit | None:
    text = _text(message)
    if not text:
        return None

    rules = [rule for rule in RULES if rule.pattern.search(text)]
    if NEGATED_REJECTION.search(text):
        rules = [rule for rule in rules if rule.name != "explicit_rejection"]
        if not any(rule.name == "conditional_acceptance" for rule in rules):
            rules.append(RULES[0])

    review_hint = None
    if MEDIA_OR_QUOTE.search(text):
        review_hint = "quoted_or_media_content"
    elif THIRD_PARTY.search(text) and not DIRECT_RELATION.search(text):
        review_hint = "third_party_content"

    if not rules and review_hint is None:
        return None
    if not rules:
        return None

    quality = _quality_factor(message)
    confidence = max(rule.base_confidence for rule in rules) * quality
    if review_hint is not None:
        confidence = min(confidence, 0.45)

    polarities = {rule.polarity for rule in rules}
    polarity = polarities.pop() if len(polarities) == 1 else "mixed"
    return Hit(
        index=index,
        message=message,
        session=session,
        evidence_ids=evidence_ids,
        types=[rule.name for rule in rules],
        polarity=polarity,
        confidence=round(confidence, 3),
        review_hint=review_hint,
    )


def _can_merge(previous: Hit, current: Hit) -> bool:
    if previous.session.session_id != current.session.session_id:
        return False
    message_distance = current.index - previous.index
    time_distance = current.message.timestamp - previous.message.timestamp
    return message_distance <= 6 or time_distance <= timedelta(minutes=30)


def _event_direction(messages: list[Message]) -> str:
    speakers = {message.sender_role.value for message in messages}
    if {"self", "target"}.issubset(speakers):
        return "mutual_discussion"
    first = messages[0]
    return f"{first.sender_role.value}_to_{first.receiver_role.value}"


def _later_followup(
    group: list[Hit],
    hits: list[Hit],
    sessions: list[Session],
) -> tuple[list[dict], list[str]]:
    last = group[-1]
    ordered_sessions = sorted(sessions, key=lambda item: item.start)
    try:
        session_index = next(i for i, item in enumerate(ordered_sessions) if item.session_id == last.session.session_id)
    except StopIteration:
        return [], []
    allowed = {item.session_id for item in ordered_sessions[session_index + 1 : session_index + 4]}
    deadline = last.message.timestamp + timedelta(days=14)
    original_polarities = {item.polarity for item in group}
    followup: list[dict] = []
    counterevidence: list[str] = []
    for hit in hits:
        if hit.index <= last.index:
            continue
        if hit.session.session_id not in allowed and hit.message.timestamp > deadline:
            continue
        followup.append(
            {
                "session_id": hit.session.session_id,
                "message_id": hit.message.message_id,
                "timestamp": hit.message.timestamp.isoformat(),
                "candidate_type": hit.types,
                "polarity": hit.polarity,
                "quote": _text(hit.message)[:280],
            }
        )
        if hit.polarity not in original_polarities and hit.polarity != "neutral":
            counterevidence.extend(hit.evidence_ids)
    return followup, list(dict.fromkeys(counterevidence))


def extract_relationship_signal_candidates(
    messages: list[Message],
    sessions: list[Session],
    evidence: list[Evidence],
) -> list[RelationshipSignalCandidate]:
    """Extract and aggregate high-recall relationship-discussion candidates."""
    ordered = sorted(messages, key=lambda item: item.timestamp)
    message_to_session = {
        message_id: session
        for session in sessions
        for message_id in session.message_ids
    }
    evidence_by_message: dict[str, list[str]] = {}
    for item in evidence:
        for message_id in item.message_ids:
            evidence_by_message.setdefault(message_id, []).append(item.evidence_id)

    hits: list[Hit] = []
    for index, message in enumerate(ordered):
        session = message_to_session.get(message.message_id)
        if session is None or message.message_type.value == "system":
            continue
        hit = _detect_hit(index, message, session, evidence_by_message.get(message.message_id, []))
        if hit is not None:
            hits.append(hit)

    groups: list[list[Hit]] = []
    for hit in hits:
        if groups and _can_merge(groups[-1][-1], hit):
            groups[-1].append(hit)
        else:
            groups.append([hit])

    index_by_id = {message.message_id: index for index, message in enumerate(ordered)}
    results: list[RelationshipSignalCandidate] = []
    for event_number, group in enumerate(groups, 1):
        trigger_messages = [item.message for item in group]
        session = group[0].session
        first_index = index_by_id[trigger_messages[0].message_id]
        last_index = index_by_id[trigger_messages[-1].message_id]
        context = [
            item
            for item in ordered[max(0, first_index - 2) : last_index + 5]
            if message_to_session.get(item.message_id, session).session_id == session.session_id
        ]
        first_speaker = trigger_messages[0].sender_role.value
        immediate_response = next(
            (
                item
                for item in ordered[last_index + 1 : last_index + 5]
                if message_to_session.get(item.message_id, session).session_id == session.session_id
                and item.sender_role.value != trigger_messages[-1].sender_role.value
            ),
            None,
        )
        followup, counterevidence = _later_followup(group, hits, sessions)
        types = list(dict.fromkeys(signal_type for item in group for signal_type in item.types))
        polarities = {item.polarity for item in group}
        confidence = round(max(item.confidence for item in group), 3)
        conditions = list(dict.fromkeys(match.group(1) for item in trigger_messages for match in CONDITION.finditer(_text(item))))
        anchors = list(dict.fromkeys(match.group(0) for item in trigger_messages for match in TIME_ANCHOR.finditer(_text(item))))
        quote = " / ".join(f"{item.sender_role.value}: {_text(item)}" for item in trigger_messages)
        results.append(
            RelationshipSignalCandidate(
                event_id=f"RS-{session.start.strftime('%Y%m%d')}-{event_number:03d}",
                evidence_ids=list(dict.fromkeys(eid for item in group for eid in item.evidence_ids)),
                candidate_type="+".join(types),
                speaker=first_speaker,
                direction=_event_direction(trigger_messages),
                quote=quote[:1000],
                context_message_ids=[item.message_id for item in context],
                response_summary=(
                    f"{immediate_response.sender_role.value}: {_text(immediate_response)[:280]}"
                    if immediate_response is not None
                    else "同一 session 内未找到对方即时回应"
                ),
                conditions=conditions,
                time_anchor=anchors,
                later_followup=followup,
                polarity=polarities.pop() if len(polarities) == 1 else "mixed",
                confidence=confidence,
                classification_status="pending_semantic_review",
                counterevidence_ids=counterevidence,
                session_id=session.session_id,
                created_at=trigger_messages[0].timestamp,
            )
        )
    return results


def finalize_relationship_signals(
    candidates: list[RelationshipSignalCandidate],
    decisions: list[RelationshipSignalDecision],
) -> list[RelationshipSignalLedgerEntry]:
    """Validate one explicit Skill decision per candidate and create the formal ledger."""
    candidate_ids = [item.event_id for item in candidates]
    decision_ids = [item.event_id for item in decisions]
    if len(decision_ids) != len(set(decision_ids)):
        raise ValueError("Duplicate relationship signal decisions are not allowed.")
    missing = sorted(set(candidate_ids) - set(decision_ids))
    unknown = sorted(set(decision_ids) - set(candidate_ids))
    if missing or unknown:
        raise ValueError(f"Decision coverage mismatch; missing={missing}, unknown={unknown}")

    by_id = {item.event_id: item for item in decisions}
    ledger: list[RelationshipSignalLedgerEntry] = []
    for candidate in candidates:
        decision = by_id[candidate.event_id]
        if decision.decision not in {"confirmed", "downgraded", "excluded"}:
            raise ValueError(f"Invalid decision for {candidate.event_id}: {decision.decision}")
        if decision.consensus_state not in {"aligned", "divergent", "open", "unanswered", "unclear"}:
            raise ValueError(
                f"Invalid consensus_state for {candidate.event_id}: {decision.consensus_state}"
            )
        if decision.decision == "excluded":
            if decision.tier is not None:
                raise ValueError(f"Excluded event {candidate.event_id} must use tier=null")
        elif decision.tier not in {"T1", "T2", "T3", "T4"}:
            raise ValueError(f"Reviewed event {candidate.event_id} requires tier T1-T4")
        if not decision.decision_reason.strip():
            raise ValueError(f"Decision reason is required for {candidate.event_id}")

        ledger.append(
            RelationshipSignalLedgerEntry(
                **candidate.model_dump(
                    exclude={"conditions", "counterevidence_ids", "classification_status"}
                ),
                classification_status=decision.decision,
                conditions=list(dict.fromkeys(candidate.conditions + decision.conditions)),
                counterevidence_ids=list(
                    dict.fromkeys(candidate.counterevidence_ids + decision.counterevidence_ids)
                ),
                decision=decision.decision,
                tier=decision.tier,
                decision_reason=decision.decision_reason,
                consensus_state=decision.consensus_state,
                boundary_effect=decision.boundary_effect,
                must_not_infer=decision.must_not_infer,
            )
        )
    return ledger


def save_relationship_signal_candidates(
    candidates: list[RelationshipSignalCandidate],
    candidate_path: Path,
) -> None:
    candidate_path.parent.mkdir(parents=True, exist_ok=True)
    write_jsonl_models(candidate_path, candidates)


def save_relationship_signal_ledger(
    ledger: list[RelationshipSignalLedgerEntry],
    ledger_path: Path,
) -> None:
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    write_jsonl_models(ledger_path, ledger)


def render_relationship_discussion_summary(
    ledger: list[RelationshipSignalLedgerEntry],
) -> str:
    """Render only explicitly reviewed relationship events."""
    included = [item for item in ledger if item.tier is not None]
    t1 = [item for item in included if item.tier == "T1"]
    excluded = [item for item in ledger if item.decision == "excluded"]
    lines = [
        "# 关系讨论摘要",
        "",
        "> 本摘要只使用已经逐条完成语义决策的关系事件。日常互动统计不能覆盖明确拒绝、边界或关系定义。",
        "",
        "## 关键关系讨论",
        "",
    ]
    if not t1:
        lines.append("- 未确认 T1 关系讨论；关系性质不足以判断。")
    for item in t1:
        lines.extend(
            [
                f"- **{item.event_id} · {item.candidate_type} · {item.consensus_state}**：{item.quote}",
                f"  - 即时回应：{item.response_summary}",
                f"  - 条件/时间：{', '.join(item.conditions + item.time_anchor) or '未明确'}",
                f"  - 边界效力：{item.boundary_effect}",
                f"  - 决策理由：{item.decision_reason}",
                f"  - 后续跟进：{len(item.later_followup)} 条；反证：{', '.join(item.counterevidence_ids) or '未记录'}",
            ]
        )
    lines.extend(["", "## 共识、分歧与开放条件", ""])
    states = {
        state: sum(item.consensus_state == state for item in t1)
        for state in ("aligned", "divergent", "open", "unanswered", "unclear")
    }
    lines.append("- 共识状态：" + "；".join(f"{name}={count}" for name, count in states.items()))
    conditions = [condition for item in t1 for condition in item.conditions]
    lines.append(f"- 开放条件：{'; '.join(dict.fromkeys(conditions)) if conditions else '未确认明确开放条件'}")
    boundaries = [item for item in t1 if item.boundary_effect not in {"", "none"}]
    lines.append(f"- 明确拒绝/边界事件：{len(boundaries)}")
    lines.extend(["", "## 能判断与不能判断", ""])
    lines.append(f"- 已纳入事件：{len(included)}；排除但留痕：{len(excluded)}。")
    lines.append("- 可以判断双方明确表达过的定义、条件和边界；不能据此读心或推断隐藏好感。")
    forbidden = list(dict.fromkeys(value for item in t1 for value in item.must_not_infer))
    if forbidden:
        lines.append(f"- 禁止推断：{'；'.join(forbidden)}")
    return "\n".join(lines) + "\n"
