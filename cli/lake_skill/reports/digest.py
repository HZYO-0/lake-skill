"""Digest generation for LakeSkill."""

from datetime import datetime
from typing import Optional

from ..schema import Message, Session


def compute_trends(
    messages: list[Message],
    sessions: list[Session],
) -> list[str]:
    """Compute temporal trends across sessions.

    Args:
        messages: List of messages
        sessions: List of sessions

    Returns:
        List of trend observation strings
    """
    trends: list[str] = []

    if len(sessions) < 2:
        return ["数据量不足，无法计算趋势（需要至少2个会话）。"]

    # Sort sessions by start time
    sorted_sessions = sorted(sessions, key=lambda s: s.start)
    mid_point = len(sorted_sessions) // 2
    first_half = sorted_sessions[:mid_point]
    second_half = sorted_sessions[mid_point:]

    # 1. Response time trend
    def calc_avg_response_time(msgs: list[Message]) -> float:
        response_times = []
        sorted_msgs = sorted(msgs, key=lambda m: m.timestamp)
        for i, msg in enumerate(sorted_msgs[1:], 1):
            prev_msg = sorted_msgs[i - 1]
            if msg.sender_role != prev_msg.sender_role:
                time_diff = (msg.timestamp - prev_msg.timestamp).total_seconds()
                if 0 < time_diff < 86400:  # Filter out gaps > 24h
                    response_times.append(time_diff)
        return sum(response_times) / len(response_times) if response_times else 0

    # Get messages for each half
    first_half_msg_ids = set()
    second_half_msg_ids = set()
    for s in first_half:
        first_half_msg_ids.update(s.message_ids)
    for s in second_half:
        second_half_msg_ids.update(s.message_ids)

    first_half_msgs = [m for m in messages if m.message_id in first_half_msg_ids]
    second_half_msgs = [m for m in messages if m.message_id in second_half_msg_ids]

    avg_rt_first = calc_avg_response_time(first_half_msgs)
    avg_rt_second = calc_avg_response_time(second_half_msgs)

    if avg_rt_first > 0 and avg_rt_second > 0:
        rt_change = (avg_rt_second - avg_rt_first) / avg_rt_first * 100
        if rt_change > 30:
            trends.append(f"回复时间呈上升趋势（增加{rt_change:.0f}%），可能表示沟通热情下降或生活节奏变化。")
        elif rt_change < -30:
            trends.append(f"回复时间呈下降趋势（减少{abs(rt_change):.0f}%），可能表示沟通频率增加。")
        else:
            trends.append("回复时间保持相对稳定。")

    # 2. Message length trend
    def calc_avg_length(msgs: list[Message], role: str) -> float:
        role_msgs = [m for m in msgs if m.sender_role.value == role and m.text]
        if not role_msgs:
            return 0
        return sum(len(m.text or "") for m in role_msgs) / len(role_msgs)

    self_len_first = calc_avg_length(first_half_msgs, "self")
    self_len_second = calc_avg_length(second_half_msgs, "self")
    target_len_first = calc_avg_length(first_half_msgs, "target")
    target_len_second = calc_avg_length(second_half_msgs, "target")

    if self_len_first > 0 and self_len_second > 0:
        self_len_change = (self_len_second - self_len_first) / self_len_first * 100
        if abs(self_len_change) > 20:
            direction = "增加" if self_len_change > 0 else "减少"
            trends.append(f"用户消息长度{direction}{abs(self_len_change):.0f}%。")

    if target_len_first > 0 and target_len_second > 0:
        target_len_change = (target_len_second - target_len_first) / target_len_first * 100
        if abs(target_len_change) > 20:
            direction = "增加" if target_len_change > 0 else "减少"
            trends.append(f"对方消息长度{direction}{abs(target_len_change):.0f}%。")

    # 3. Session frequency trend
    if len(first_half) >= 1 and len(second_half) >= 1:
        first_duration = (first_half[-1].end - first_half[0].start).days or 1
        second_duration = (second_half[-1].end - second_half[0].start).days or 1
        first_freq = len(first_half) / first_duration
        second_freq = len(second_half) / second_duration

        if first_freq > 0 and second_freq > 0:
            freq_change = (second_freq - first_freq) / first_freq * 100
            if freq_change > 30:
                trends.append(f"会话频率呈上升趋势（增加{freq_change:.0f}%），互动更加频繁。")
            elif freq_change < -30:
                trends.append(f"会话频率呈下降趋势（减少{abs(freq_change):.0f}%），互动减少。")

    # 4. Initiation pattern
    first_self_count = sum(s.self_count for s in first_half)
    first_target_count = sum(s.target_count for s in first_half)
    second_self_count = sum(s.self_count for s in second_half)
    second_target_count = sum(s.target_count for s in second_half)

    if first_self_count > 0 and first_target_count > 0:
        first_ratio = first_self_count / (first_self_count + first_target_count)
        if second_self_count > 0 and second_target_count > 0:
            second_ratio = second_self_count / (second_self_count + second_target_count)
            ratio_change = second_ratio - first_ratio
            if ratio_change > 0.15:
                trends.append("用户发起对话的比例增加，可能表示用户更加主动。")
            elif ratio_change < -0.15:
                trends.append("对方发起对话的比例增加，可能表示对方更加主动。")

    # 5. Emotion trajectory
    first_risk = [s for s in first_half if s.risk_level == "high"]
    second_risk = [s for s in second_half if s.risk_level == "high"]
    if len(first_risk) > 0 and len(second_risk) == 0:
        trends.append("高风险会话减少，关系可能趋于稳定。")
    elif len(first_risk) == 0 and len(second_risk) > 0:
        trends.append("高风险会话增加，需要关注关系变化。")

    first_repair = [s for s in first_half if s.episode_type and "repair" in s.episode_type]
    second_repair = [s for s in second_half if s.episode_type and "repair" in s.episode_type]
    if len(second_repair) > len(first_repair):
        trends.append("修复行为增加，关系可能正在改善。")

    if not trends:
        trends.append("未检测到显著的时间趋势变化。")

    return trends


def generate_digest(
    messages: list[Message],
    sessions: list[Session],
    output_path: Optional[str] = None,
) -> str:
    """Generate relationship digest.

    Args:
        messages: List of messages
        sessions: List of sessions
        output_path: Optional output file path

    Returns:
        Digest markdown string
    """
    # Calculate statistics
    total_messages = len(messages)
    self_messages = [m for m in messages if m.sender_role.value == "self"]
    target_messages = [m for m in messages if m.sender_role.value == "target"]

    # Get time range
    if messages:
        start_time = min(m.timestamp for m in messages)
        end_time = max(m.timestamp for m in messages)
        duration_days = (end_time - start_time).days
    else:
        start_time = end_time = datetime.now()
        duration_days = 0

    # Build digest
    lines = [
        "# Relationship Digest",
        "",
        "## Data Summary",
        "",
        f"- **Total Messages**: {total_messages}",
        f"- **Self Messages**: {len(self_messages)}",
        f"- **Target Messages**: {len(target_messages)}",
        f"- **Sessions**: {len(sessions)}",
        f"- **Time Range**: {start_time.strftime('%Y-%m-%d')} to {end_time.strftime('%Y-%m-%d')}",
        f"- **Duration**: {duration_days} days",
        "",
    ]

    # Add session summaries
    if sessions:
        lines.append("## Sessions")
        lines.append("")

        for session in sessions:
            lines.append(f"### Session {session.session_id}")
            lines.append("")
            lines.append(f"- **Time**: {session.start.strftime('%Y-%m-%d %H:%M')} - {session.end.strftime('%Y-%m-%d %H:%M')}")
            lines.append(f"- **Messages**: {session.message_count}")
            lines.append(f"- **Self**: {session.self_count}, **Target**: {session.target_count}")

            if session.topic:
                lines.append(f"- **Topic**: {session.topic}")
            if session.episode_type:
                lines.append(f"- **Episode Type**: {', '.join(session.episode_type)}")
            if session.risk_level:
                lines.append(f"- **Risk Level**: {session.risk_level}")

            lines.append("")

    # Add message patterns
    lines.append("## Message Patterns")
    lines.append("")

    # Analyze response patterns
    if self_messages and target_messages:
        # Calculate average response time
        response_times = []
        for i, msg in enumerate(messages[1:], 1):
            prev_msg = messages[i - 1]
            if msg.sender_role != prev_msg.sender_role:
                time_diff = (msg.timestamp - prev_msg.timestamp).total_seconds()
                response_times.append(time_diff)

        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            lines.append(f"- **Average Response Time**: {avg_response_time:.0f} seconds")

        # Calculate message length statistics
        self_lengths = [len(m.text or "") for m in self_messages]
        target_lengths = [len(m.text or "") for m in target_messages]

        if self_lengths:
            avg_self_length = sum(self_lengths) / len(self_lengths)
            lines.append(f"- **Average Self Message Length**: {avg_self_length:.0f} characters")

        if target_lengths:
            avg_target_length = sum(target_lengths) / len(target_lengths)
            lines.append(f"- **Average Target Message Length**: {avg_target_length:.0f} characters")

    lines.append("")

    # Add key quotes
    key_quotes = extract_key_quotes(messages)
    if key_quotes:
        lines.append("## Key Quotes")
        lines.append("")
        for quote in key_quotes:
            speaker_label = "Self" if quote["speaker"] == "self" else "Target"
            lines.append(f"- **[{speaker_label}]** {quote['text']}")
        lines.append("")

    # Add notes
    lines.append("## Notes")
    lines.append("")
    lines.append("- This digest is generated from redacted data.")
    lines.append("- Evidence IDs should be used for detailed analysis.")
    lines.append("- Confidence levels are based on message patterns.")

    # Add temporal trends (A5)
    if sessions and len(sessions) >= 2:
        lines.append("")
        lines.append("## 时间趋势")
        lines.append("")
        trends = compute_trends(messages, sessions)
        for trend in trends:
            lines.append(f"- {trend}")

    digest = "\n".join(lines)

    # Save to file if path provided
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(digest)

    return digest


def extract_key_quotes(messages: list[Message], max_quotes: int = 10) -> list[dict]:
    """Extract key quotes from messages.

    Args:
        messages: List of messages
        max_quotes: Maximum number of quotes to extract

    Returns:
        List of quote dictionaries
    """
    quotes = []

    # Simple extraction based on message length and content
    for msg in messages:
        if not msg.text:
            continue

        # Skip very short messages
        if len(msg.text) < 10:
            continue

        # Look for emotional or important content
        important_keywords = ["喜欢", "爱", "想", "生气", "难过", "开心", "分手", "和好"]
        if any(kw in msg.text for kw in important_keywords):
            quotes.append({
                "message_id": msg.message_id,
                "speaker": msg.sender_role.value,
                "text": msg.text[:200],  # Limit length
                "timestamp": msg.timestamp.isoformat(),
            })

            if len(quotes) >= max_quotes:
                break

    return quotes
