"""End-to-end tests for candidate extraction and explicit semantic finalization."""

from datetime import datetime, timedelta, timezone

import pytest

from lake_skill.evidence.indexer import index_evidence
from lake_skill.relationship_signals import (
    extract_relationship_signal_candidates,
    finalize_relationship_signals,
    render_relationship_discussion_summary,
)
from lake_skill.schema import (
    Message,
    MessageType,
    Modality,
    QualityInfo,
    RelationshipSignalDecision,
    SenderRole,
)
from lake_skill.segmentation.sessionizer import segment_sessions


def _messages(rows, start=None):
    start = start or datetime(2026, 7, 1, 9, 0, tzinfo=timezone.utc)
    return [
        Message(
            message_id=f"m{index + 1}",
            conversation_id="c1",
            source_type="test",
            timestamp=start + timedelta(minutes=minute),
            sender_role=SenderRole(speaker),
            receiver_role=SenderRole.TARGET if speaker == "self" else SenderRole.SELF,
            message_type=MessageType.TEXT,
            modality=Modality.TEXT,
            text=text,
        )
        for index, (speaker, text, minute) in enumerate(rows)
    ]


def _extract(rows):
    messages = _messages(rows)
    sessions = segment_sessions(messages)
    evidence = index_evidence(messages, sessions)
    return extract_relationship_signal_candidates(messages, sessions, evidence)


def _finalize(candidates, *, state="open", effect="none"):
    decisions = [
        RelationshipSignalDecision(
            event_id=item.event_id,
            decision="confirmed",
            tier="T1",
            decision_reason="上下文支持该关系讨论事件。",
            consensus_state=state,
            boundary_effect=effect,
            conditions=item.conditions,
            must_not_infer=["不能推断隐藏好感"],
        )
        for item in candidates
    ]
    return finalize_relationship_signals(candidates, decisions)


def test_question_pause_and_condition_are_one_pending_event():
    candidates = _extract(
        [
            ("self", "我们是什么关系", 0),
            ("target", "我现在没办法开始", 2),
            ("target", "等工作稳定再说", 4),
            ("self", "我明白了，会尊重你的节奏", 5),
        ]
    )
    assert len(candidates) == 1
    event = candidates[0]
    assert "relationship_definition" in event.candidate_type
    assert "pause_or_downgrade" in event.candidate_type
    assert "conditional_acceptance" in event.candidate_type
    assert "工作稳定" in "".join(event.conditions)
    assert event.response_summary.startswith("self:")
    assert event.classification_status == "pending_semantic_review"


def test_friends_is_definition_and_boundary_candidate():
    candidates = _extract([("target", "我们先做朋友", 0)])
    assert "relationship_definition" in candidates[0].candidate_type
    assert "pause_or_downgrade" in candidates[0].candidate_type


def test_double_negative_is_not_plain_rejection():
    candidates = _extract([("target", "不是不喜欢你，只是不想现在开始", 0)])
    assert "conditional_acceptance" in candidates[0].candidate_type
    assert "explicit_rejection" not in candidates[0].candidate_type


def test_third_party_marriage_is_not_our_commitment():
    assert _extract([("target", "我朋友要结婚了", 0)]) == []


def test_rejection_and_later_reopening_remain_two_phases():
    candidates = _extract(
        [
            ("target", "我不喜欢你，不想和你在一起", 0),
            ("self", "我知道了", 1),
            ("target", "今天工作挺忙", 60 * 24 * 2),
            ("target", "我想和你在一起，我们重新开始吧", 60 * 24 * 20),
        ]
    )
    assert len(candidates) == 2
    assert "explicit_rejection" in candidates[0].candidate_type
    assert "confession_or_progression" in candidates[1].candidate_type
    assert candidates[0].later_followup


def test_daily_chat_does_not_override_finalized_rejection():
    candidates = _extract(
        [
            ("target", "我不喜欢你，不想和你在一起", 0),
            ("target", "今天吃什么", 10),
            ("self", "面条", 11),
        ]
    )
    ledger = _finalize(candidates, state="aligned", effect="stop_progression")
    summary = render_relationship_discussion_summary(ledger)
    assert "明确拒绝/边界事件：1" in summary
    assert "不能据此读心" in summary


def test_lyrics_and_low_quality_remain_pending_low_confidence():
    lyric = _extract([("target", "歌词里说我们以后结婚", 0)])[0]
    assert lyric.classification_status == "pending_semantic_review"
    assert lyric.confidence <= 0.45

    messages = _messages([("target", "我们先做朋友", 0)])
    messages[0].quality = QualityInfo(ocr_confidence=0.4)
    sessions = segment_sessions(messages)
    evidence = index_evidence(messages, sessions)
    candidate = extract_relationship_signal_candidates(messages, sessions, evidence)[0]
    assert candidate.confidence < 0.72
    assert candidate.classification_status == "pending_semantic_review"


def test_finalize_requires_complete_decisions_and_retains_exclusions():
    candidates = _extract(
        [
            ("self", "我喜欢你，想和你在一起", 0),
            ("target", "我不确定，以后再说", 2),
        ]
    )
    with pytest.raises(ValueError, match="coverage mismatch"):
        finalize_relationship_signals(candidates, [])

    decisions = [
        RelationshipSignalDecision(
            event_id=candidates[0].event_id,
            decision="excluded",
            tier=None,
            decision_reason="测试排除并保留。",
            consensus_state="unclear",
            boundary_effect="none",
        )
    ]
    ledger = finalize_relationship_signals(candidates, decisions)
    assert ledger[0].decision == "excluded"
    assert ledger[0].tier is None
