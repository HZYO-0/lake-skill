"""Productization tests for windows, T4 stats, reports, workspaces and demos."""

import json
from datetime import datetime, timedelta, timezone

from lake_skill.analysis_windows import build_analysis_windows
from lake_skill.demo_assets import generate_product_scenarios
from lake_skill.interaction_stats import compute_interaction_stats
from lake_skill.reports.analysis import (
    build_relationship_analysis,
    render_analysis_html,
    render_analysis_markdown,
)
from lake_skill.schema import (
    Message,
    MessageType,
    Modality,
    RelationshipSignalCandidate,
    RelationshipSignalLedgerEntry,
    SenderRole,
)
from lake_skill.segmentation.sessionizer import segment_sessions
from lake_skill.workspace import contact_workspace, resolve_text_route, write_workspace_state


def _message(index, minute, role, text):
    return Message(
        message_id=f"m{index}",
        conversation_id="c",
        source_type="test",
        timestamp=datetime(2026, 1, 1, tzinfo=timezone.utc) + timedelta(minutes=minute),
        sender_role=SenderRole(role),
        receiver_role=SenderRole.TARGET if role == "self" else SenderRole.SELF,
        message_type=MessageType.TEXT,
        modality=Modality.TEXT,
        text=text,
    )


def test_recent_window_uses_coverage_tail_and_event_is_never_sampled():
    messages = [
        _message(index, index, "self" if index % 2 else "target", f"消息 {index}")
        for index in range(1, 251)
    ]
    sessions = segment_sessions(messages)
    candidate = RelationshipSignalCandidate(
        event_id="RS-MIDDLE",
        candidate_type="relationship_definition",
        speaker="target",
        quote="我们先做朋友",
        context_message_ids=["m119", "m120", "m121"],
        session_id=sessions[0].session_id,
        created_at=messages[119].timestamp,
    )
    windows = build_analysis_windows(messages, sessions, [candidate], recent_limit=20)
    event = next(item for item in windows if item["window_type"] == "relationship_discussion")
    recent = next(item for item in windows if item["window_type"] == "recent")
    assert event["message_ids"] == ["m119", "m120", "m121"]
    assert event["full_retention"] is True
    assert recent["message_ids"][0] == "m231"
    assert recent["message_ids"][-1] == "m250"


def test_interaction_stats_are_descriptive_t4_without_scores():
    messages = [
        _message(1, 0, "self", "早"),
        _message(2, 2, "target", "早"),
        _message(3, 10, "self", "今天忙吗"),
        _message(4, 20, "target", "有一点"),
    ]
    stats = compute_interaction_stats(messages, segment_sessions(messages))
    encoded = json.dumps(stats, ensure_ascii=False)
    assert stats["metric_tier"] == "T4"
    assert stats["response_time_seconds"]["sample_size"] == 3
    assert all(term not in encoded for term in ("被爱指数", "舔狗指数", "冷淡指数"))


def _rejection_ledger():
    return [
        RelationshipSignalLedgerEntry(
            event_id="RS-1",
            candidate_type="explicit_rejection",
            speaker="target",
            direction="target_to_self",
            quote="target: 我不喜欢你，不想和你在一起",
            context_message_ids=["m1"],
            response_summary="self: 我会尊重",
            polarity="negative",
            confidence=0.95,
            classification_status="confirmed",
            session_id="S1",
            created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
            decision="confirmed",
            tier="T1",
            decision_reason="明确拒绝。",
            consensus_state="aligned",
            boundary_effect="stop_progression",
            must_not_infer=["不能推断隐藏好感"],
        )
    ]


def test_markdown_and_html_share_analysis_and_respect_rejection():
    analysis = build_relationship_analysis(
        ledger=_rejection_ledger(),
        interaction_stats={"coverage": {"message_count": 999, "session_count": 20}},
    )
    markdown = render_analysis_markdown(analysis)
    html = render_analysis_html(analysis)
    quote = "我不喜欢你，不想和你在一起"
    assert quote in markdown and quote in html
    assert "不再从日常聊天中反推隐藏好感" in analysis["action_brief"]["this_week"]
    assert "http://" not in html and "https://" not in html
    assert "爱情总分" in markdown


def test_contact_workspaces_are_isolated_and_routes_work(tmp_path):
    first = contact_workspace(tmp_path, "小王")
    second = contact_workspace(tmp_path, "小李")
    assert first != second
    first.mkdir(parents=True)
    source = tmp_path / "chat.csv"
    source.write_text("synthetic", encoding="utf-8")
    write_workspace_state(
        first, source=source, mode="quick", privacy_mode="local-safe", message_count=1
    )
    state = json.loads((first / "workspace_state.json").read_text(encoding="utf-8"))
    assert state["message_count"] == 1
    assert resolve_text_route("/急") == "quick"
    assert resolve_text_route("/深度") == "deep"
    assert resolve_text_route("/画像") == "profile"


def test_four_synthetic_demo_scenarios_generate_same_source_reports(tmp_path):
    generate_product_scenarios(tmp_path)
    names = {
        "conditional-acceptance",
        "rejection-with-daily-chat",
        "divergent-definition",
        "reopening-after-breakup",
    }
    for name in names:
        root = tmp_path / "scenarios" / name
        analysis = json.loads((root / "relationship_analysis.json").read_text(encoding="utf-8"))
        markdown = (root / "relationship_analysis.md").read_text(encoding="utf-8")
        html = (root / "relationship_analysis.html").read_text(encoding="utf-8")
        assert analysis["review_status"] == "finalized"
        assert analysis["critical_relationship_discussions"]
        event_id = analysis["critical_relationship_discussions"][0]["event_id"]
        assert event_id in markdown and event_id in html
