"""Session segmentation for LakeSkill."""

from datetime import datetime, timedelta
from typing import Optional

from ..schema import Message, Session


def segment_sessions(
    messages: list[Message],
    time_gap_hours: float = 6.0,
    long_gap_hours: float = 24.0,
) -> list[Session]:
    """Segment messages into sessions based on time gaps.

    Args:
        messages: List of messages (must be sorted by timestamp)
        time_gap_hours: Time gap threshold for session split (hours)
        long_gap_hours: Long gap threshold for marking sessions after long pauses

    Returns:
        List of sessions
    """
    if not messages:
        return []

    # Ensure messages are sorted by timestamp
    messages = sorted(messages, key=lambda m: m.timestamp)

    sessions: list[Session] = []
    current_session_messages: list[Message] = []
    session_start: Optional[datetime] = None
    session_count = 0
    last_session_end: Optional[datetime] = None

    for i, msg in enumerate(messages):
        # First message
        if not current_session_messages:
            current_session_messages.append(msg)
            session_start = msg.timestamp
            continue

        # Check time gap
        last_msg = current_session_messages[-1]
        time_diff = msg.timestamp - last_msg.timestamp
        gap_threshold = timedelta(hours=time_gap_hours)

        if time_diff > gap_threshold:
            # Create session from accumulated messages
            session = _create_session(
                current_session_messages,
                session_count + 1,
                session_start,
                last_session_end,
                long_gap_hours,
            )
            sessions.append(session)

            # Start new session
            session_count += 1
            last_session_end = current_session_messages[-1].timestamp
            current_session_messages = [msg]
            session_start = msg.timestamp
        else:
            current_session_messages.append(msg)

    # Create last session
    if current_session_messages:
        session = _create_session(
            current_session_messages,
            session_count + 1,
            session_start,
            last_session_end,
            long_gap_hours,
        )
        sessions.append(session)

    return sessions


def _create_session(
    messages: list[Message],
    session_num: int,
    start_time: Optional[datetime],
    last_session_end: Optional[datetime] = None,
    long_gap_hours: float = 24.0,
) -> Session:
    """Create a session from messages.

    Args:
        messages: List of messages
        session_num: Session number
        start_time: Session start time
        last_session_end: End time of previous session (for gap detection)
        long_gap_hours: Long gap threshold for marking sessions after long pauses

    Returns:
        Session object
    """
    if not messages:
        raise ValueError("Cannot create session from empty messages")

    # Calculate statistics
    self_count = sum(1 for m in messages if m.sender_role.value == "self")
    target_count = sum(1 for m in messages if m.sender_role.value == "target")

    # Determine session time range
    start = start_time or messages[0].timestamp
    end = messages[-1].timestamp

    # Generate session ID
    session_id = f"S-{start.strftime('%Y%m%d')}-{session_num:03d}"

    # Get conversation ID
    conversation_id = messages[0].conversation_id

    # Get message IDs
    message_ids = [m.message_id for m in messages]

    # Detect long gap from previous session
    episode_type: list[str] = []
    if last_session_end is not None:
        gap = (start - last_session_end).total_seconds() / 3600
        if gap >= long_gap_hours:
            episode_type.append("long_pause")

    return Session(
        session_id=session_id,
        conversation_id=conversation_id,
        start=start,
        end=end,
        message_count=len(messages),
        self_count=self_count,
        target_count=target_count,
        message_ids=message_ids,
        episode_type=episode_type,
    )


def get_session_summary(session: Session) -> dict:
    """Get session summary.

    Args:
        session: Session object

    Returns:
        Summary dictionary
    """
    return {
        "session_id": session.session_id,
        "start": session.start.isoformat(),
        "end": session.end.isoformat(),
        "duration_hours": (session.end - session.start).total_seconds() / 3600,
        "message_count": session.message_count,
        "self_count": session.self_count,
        "target_count": session.target_count,
        "topic": session.topic,
        "episode_type": session.episode_type,
        "risk_level": session.risk_level,
    }
