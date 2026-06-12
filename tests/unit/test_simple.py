"""Basic smoke tests for LakeSkill."""

from datetime import datetime, timezone

from lake_skill import __version__
from lake_skill.schema import Message, SenderRole, MessageType, Modality


def test_version_string():
    """Version follows semver format."""
    parts = __version__.split(".")
    assert len(parts) == 3
    assert all(p.isdigit() for p in parts)


def test_message_creation():
    """Message model can be created with required fields."""
    msg = Message(
        message_id="test_001",
        conversation_id="conv_001",
        source_type="csv",
        timestamp=datetime(2026, 6, 1, 12, 0, 0, tzinfo=timezone.utc),
        sender_id="user_a",
        sender_role=SenderRole.SELF,
        text="Hello",
        message_type=MessageType.TEXT,
        modality=Modality.TEXT,
    )
    assert msg.message_id == "test_001"
    assert msg.sender_role == SenderRole.SELF
    assert msg.text == "Hello"


def test_message_serialization():
    """Message can be serialized to dict."""
    msg = Message(
        message_id="test_002",
        conversation_id="conv_001",
        source_type="csv",
        timestamp=datetime(2026, 6, 1, 12, 0, 0, tzinfo=timezone.utc),
        sender_id="user_a",
        sender_role=SenderRole.TARGET,
        text="Test message",
        message_type=MessageType.TEXT,
        modality=Modality.TEXT,
    )
    d = msg.model_dump()
    assert d["message_id"] == "test_002"
    assert d["sender_role"] == "target"
    assert d["text"] == "Test message"


def test_sender_role_enum():
    """SenderRole has expected values."""
    assert SenderRole.SELF.value == "self"
    assert SenderRole.TARGET.value == "target"
    assert SenderRole.OTHER.value == "other"
    assert SenderRole.UNKNOWN.value == "unknown"


def test_message_type_enum():
    """MessageType has expected values."""
    assert MessageType.TEXT.value == "text"
    assert MessageType.IMAGE.value == "image"
    assert MessageType.VOICE.value == "voice"
