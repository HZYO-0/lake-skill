"""Priority-ordered analysis windows with full retention of relationship discussions."""

from __future__ import annotations

from .schema import Message, RelationshipSignalCandidate, Session


def build_analysis_windows(
    messages: list[Message],
    sessions: list[Session],
    candidates: list[RelationshipSignalCandidate],
    *,
    recent_limit: int = 200,
) -> list[dict]:
    ordered = sorted(messages, key=lambda item: item.timestamp)
    by_id = {item.message_id: item for item in ordered}
    windows: list[dict] = []

    for candidate in candidates:
        windows.append(
            {
                "window_id": f"W-EVENT-{candidate.event_id}",
                "priority": 1,
                "window_type": "relationship_discussion",
                "event_id": candidate.event_id,
                "message_ids": candidate.context_message_ids,
                "full_retention": True,
                "reason": "all relationship discussion candidates precede sampling",
            }
        )
        if candidate.later_followup or candidate.counterevidence_ids:
            followup_ids = [
                item["message_id"] for item in candidate.later_followup if item.get("message_id")
            ]
            windows.append(
                {
                    "window_id": f"W-FOLLOWUP-{candidate.event_id}",
                    "priority": 2,
                    "window_type": "reversal_fulfillment_withdrawal_or_counterevidence",
                    "event_id": candidate.event_id,
                    "message_ids": list(dict.fromkeys(candidate.context_message_ids + followup_ids)),
                    "full_retention": True,
                }
            )

    for session in sorted(sessions, key=lambda item: item.start):
        if session.risk_level == "high" or any(
            name in {"conflict", "repair", "breakup"} for name in session.episode_type
        ):
            windows.append(
                {
                    "window_id": f"W-CONFLICT-{session.session_id}",
                    "priority": 4,
                    "window_type": "conflict_or_repair",
                    "session_id": session.session_id,
                    "message_ids": session.message_ids,
                    "full_retention": False,
                }
            )

    if sessions:
        first = min(sessions, key=lambda item: item.start)
        windows.append(
            {
                "window_id": "W-ORIGIN",
                "priority": 5,
                "window_type": "relationship_origin",
                "session_id": first.session_id,
                "message_ids": first.message_ids,
                "full_retention": False,
            }
        )

    recent = ordered[-recent_limit:]
    windows.append(
        {
            "window_id": "W-RECENT",
            "priority": 6,
            "window_type": "recent",
            "message_ids": [item.message_id for item in recent],
            "start": recent[0].timestamp.isoformat() if recent else None,
            "end": recent[-1].timestamp.isoformat() if recent else None,
            "selection_rule": f"last {recent_limit} messages from coverage end",
            "full_retention": False,
        }
    )

    event_message_ids = {message_id for item in candidates for message_id in item.context_message_ids}
    representative = [
        item.message_id
        for item in ordered
        if item.message_id not in event_message_ids and item.message_id in by_id
    ][:: max(1, len(ordered) // 100 or 1)][:100]
    windows.append(
        {
            "window_id": "W-DAILY",
            "priority": 7,
            "window_type": "representative_daily_interaction",
            "message_ids": representative,
            "full_retention": False,
        }
    )
    return sorted(windows, key=lambda item: (item["priority"], item["window_id"]))
