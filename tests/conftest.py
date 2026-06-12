"""Shared test fixtures for LakeSkill."""

from datetime import datetime, timezone

import pytest

from lake_skill.schema import Message, SenderRole, MessageType, Modality


@pytest.fixture
def tmp_dir(tmp_path):
    """Provide a temporary directory for test outputs."""
    return tmp_path


@pytest.fixture
def sample_message():
    """Create a single sample message."""
    return Message(
        message_id="msg_001",
        conversation_id="conv_001",
        source_type="csv",
        timestamp=datetime(2026, 6, 1, 12, 0, 0, tzinfo=timezone.utc),
        sender_id="user_a",
        sender_role=SenderRole.SELF,
        text="Hello, how are you?",
        message_type=MessageType.TEXT,
        modality=Modality.TEXT,
    )


@pytest.fixture
def sample_messages():
    """Create a list of sample messages for testing."""
    base_time = datetime(2026, 6, 1, 10, 0, 0, tzinfo=timezone.utc)
    messages = []
    for i in range(10):
        messages.append(Message(
            message_id=f"msg_{i:03d}",
            conversation_id="conv_001",
            source_type="csv",
            timestamp=datetime.fromtimestamp(
                base_time.timestamp() + i * 300, tz=timezone.utc
            ),
            sender_id="user_a" if i % 2 == 0 else "user_b",
            sender_role=SenderRole.SELF if i % 2 == 0 else SenderRole.TARGET,
            text=f"Message {i}",
            message_type=MessageType.TEXT,
            modality=Modality.TEXT,
        ))
    return messages
