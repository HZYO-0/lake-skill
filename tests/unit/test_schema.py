"""Tests for data schemas."""

from datetime import datetime, timezone


from lake_skill.schema import (
    Message,
    QualityInfo,
    MessageType,
    SenderRole,
    Modality,
    Session,
    IntakeCard,
)
from lake_skill import __version__


class TestMessage:
    def test_create_with_required_fields(self):
        msg = Message(
            message_id="m1",
            conversation_id="c1",
            source_type="csv",
            timestamp=datetime(2026, 6, 1, tzinfo=timezone.utc),
            sender_id="u1",
            sender_role=SenderRole.SELF,
            text="hello",
            message_type=MessageType.TEXT,
            modality=Modality.TEXT,
        )
        assert msg.message_id == "m1"
        assert msg.sender_role == SenderRole.SELF

    def test_default_quality(self):
        msg = Message(
            message_id="m1",
            conversation_id="c1",
            source_type="csv",
            timestamp=datetime(2026, 6, 1, tzinfo=timezone.utc),
            sender_id="u1",
            sender_role=SenderRole.SELF,
            text="hello",
            message_type=MessageType.TEXT,
            modality=Modality.TEXT,
        )
        assert msg.quality is not None
        assert isinstance(msg.quality, QualityInfo)

    def test_sender_role_values(self):
        assert SenderRole.SELF.value == "self"
        assert SenderRole.TARGET.value == "target"
        assert SenderRole.OTHER.value == "other"
        assert SenderRole.UNKNOWN.value == "unknown"

    def test_message_type_values(self):
        assert MessageType.TEXT.value == "text"
        assert MessageType.IMAGE.value == "image"
        assert MessageType.VOICE.value == "voice"
        assert MessageType.VIDEO.value == "video"
        assert MessageType.FILE.value == "file"

    def test_modality_values(self):
        assert Modality.TEXT.value == "text"
        assert Modality.AUDIO.value == "audio"
        assert Modality.IMAGE.value == "image"

    def test_serialization_roundtrip(self):
        msg = Message(
            message_id="m1",
            conversation_id="c1",
            source_type="csv",
            timestamp=datetime(2026, 6, 1, tzinfo=timezone.utc),
            sender_id="u1",
            sender_role=SenderRole.TARGET,
            text="test",
            message_type=MessageType.TEXT,
            modality=Modality.TEXT,
        )
        d = msg.model_dump()
        msg2 = Message(**d)
        assert msg2.message_id == msg.message_id
        assert msg2.sender_role == msg.sender_role
        assert msg2.text == msg.text


class TestSession:
    def test_create_session(self):
        now = datetime(2026, 6, 1, tzinfo=timezone.utc)
        session = Session(
            session_id="S-20260601-001",
            conversation_id="c1",
            start=now,
            end=now,
            message_count=0,
            messages=[],
        )
        assert session.session_id == "S-20260601-001"


class TestIntakeCard:
    def test_default_version(self):
        card = IntakeCard()
        assert card.version == __version__

    def test_default_privacy_mode(self):
        card = IntakeCard()
        assert card.privacy_mode == "cloud-safe"


class TestQualityInfo:
    def test_default_quality(self):
        q = QualityInfo()
        assert q.asr_confidence is None
        assert q.ocr_confidence is None
