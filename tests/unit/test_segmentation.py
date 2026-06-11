"""Tests for segmentation."""

from datetime import datetime, timedelta

from lake_skill.schema import Message, SenderRole, MessageType, Modality
from lake_skill.segmentation.sessionizer import segment_sessions


def create_message(minutes_offset: int, sender: str = "target") -> Message:
    """Create a test message with time offset."""
    base_time = datetime(2025, 5, 21, 22, 0, 0)
    return Message(
        message_id=f"m_{minutes_offset:03d}",
        conversation_id="default",
        source_type="test",
        timestamp=base_time + timedelta(minutes=minutes_offset),
        sender_role=SenderRole(sender),
        message_type=MessageType.TEXT,
        modality=Modality.TEXT,
        text=f"Message {minutes_offset}",
    )


def test_segment_sessions_basic():
    """Test basic session segmentation."""
    messages = [
        create_message(0),
        create_message(1),
        create_message(2),
        create_message(10),  # 8 minute gap - should be same session
        create_message(11),
    ]

    sessions = segment_sessions(messages, time_gap_hours=1.0)
    assert len(sessions) == 1


def test_segment_sessions_time_gap():
    """Test session segmentation with time gap."""
    messages = [
        create_message(0),
        create_message(1),
        create_message(120),  # 2 hour gap - should be new session
        create_message(121),
    ]

    sessions = segment_sessions(messages, time_gap_hours=1.0)
    assert len(sessions) == 2


def test_segment_sessions_empty():
    """Test session segmentation with empty messages."""
    messages = []
    sessions = segment_sessions(messages)
    assert len(sessions) == 0


def test_segment_sessions_single_message():
    """Test session segmentation with single message."""
    messages = [create_message(0)]
    sessions = segment_sessions(messages)
    assert len(sessions) == 1
    assert sessions[0].message_count == 1
