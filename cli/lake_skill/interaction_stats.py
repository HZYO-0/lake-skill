"""Descriptive interaction statistics. These metrics are T4 context, never relationship scores."""

from __future__ import annotations

from datetime import timedelta
from math import ceil
from statistics import median

from .schema import Message, Session


def _percentile(values: list[float], percentile: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    index = max(0, ceil(percentile * len(ordered)) - 1)
    return round(ordered[index], 2)


def _period_counts(messages: list[Message], days: int) -> dict:
    if not messages:
        return {"days": days, "messages": 0, "self": 0, "target": 0}
    cutoff = max(item.timestamp for item in messages) - timedelta(days=days)
    selected = [item for item in messages if item.timestamp >= cutoff]
    return {
        "days": days,
        "messages": len(selected),
        "self": sum(item.sender_role.value == "self" for item in selected),
        "target": sum(item.sender_role.value == "target" for item in selected),
    }


def compute_interaction_stats(messages: list[Message], sessions: list[Session]) -> dict:
    """Compute transparent full-corpus descriptive metrics without affection scores."""
    ordered = sorted(messages, key=lambda item: item.timestamp)
    response_seconds: list[float] = []
    streaks: list[int] = []
    long_gaps: list[dict] = []
    current_streak = 0
    previous_role = None

    for index, item in enumerate(ordered):
        role = item.sender_role.value
        if role == previous_role:
            current_streak += 1
        else:
            if current_streak:
                streaks.append(current_streak)
            current_streak = 1
            if index:
                gap = (item.timestamp - ordered[index - 1].timestamp).total_seconds()
                if 0 < gap <= 86400:
                    response_seconds.append(gap)
                if gap > 86400:
                    long_gaps.append(
                        {
                            "after_message_id": ordered[index - 1].message_id,
                            "restart_message_id": item.message_id,
                            "gap_hours": round(gap / 3600, 2),
                            "restart_by": role,
                        }
                    )
        previous_role = role
    if current_streak:
        streaks.append(current_streak)

    by_id = {item.message_id: item for item in ordered}
    initiators = [
        by_id[session.message_ids[0]].sender_role.value
        for session in sessions
        if session.message_ids and session.message_ids[0] in by_id
    ]
    text_lengths = {
        role: [
            len((item.text_redacted or item.text or "").strip())
            for item in ordered
            if item.sender_role.value == role and (item.text_redacted or item.text)
        ]
        for role in ("self", "target")
    }

    return {
        "metric_tier": "T4",
        "policy": "Descriptive context only; explicit relationship discussions and boundaries take priority.",
        "coverage": {
            "message_count": len(ordered),
            "session_count": len(sessions),
            "start": ordered[0].timestamp.isoformat() if ordered else None,
            "end": ordered[-1].timestamp.isoformat() if ordered else None,
        },
        "session_initiation": {
            "self": sum(item == "self" for item in initiators),
            "target": sum(item == "target" for item in initiators),
            "other": sum(item not in {"self", "target"} for item in initiators),
            "denominator": len(initiators),
            "formula": "sessions initiated by role / sessions with a resolvable first message",
        },
        "response_time_seconds": {
            "median": round(median(response_seconds), 2) if response_seconds else None,
            "p90": _percentile(response_seconds, 0.90),
            "sample_size": len(response_seconds),
            "exclusion_rule": "role changes only; exclude non-positive gaps and gaps over 24 hours",
        },
        "message_distribution": {
            role: {
                "count": sum(item.sender_role.value == role for item in ordered),
                "median_text_length": round(median(values), 2) if values else None,
            }
            for role, values in text_lengths.items()
        },
        "consecutive_send_distribution": {
            "median": round(median(streaks), 2) if streaks else None,
            "p90": _percentile([float(item) for item in streaks], 0.90),
            "sample_size": len(streaks),
            "formula": "consecutive messages by the same sender",
        },
        "long_gaps_and_repairs": {
            "threshold_hours": 24,
            "count": len(long_gaps),
            "restart_by_self": sum(item["restart_by"] == "self" for item in long_gaps),
            "restart_by_target": sum(item["restart_by"] == "target" for item in long_gaps),
            "events": long_gaps,
        },
        "recent_windows": {str(days): _period_counts(ordered, days) for days in (14, 30, 90)},
    }
