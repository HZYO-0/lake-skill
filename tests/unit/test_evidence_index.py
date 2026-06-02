"""Tests for evidence indexing."""

from datetime import datetime

from bondlens.schema import Message, Session, SenderRole, MessageType, Modality
from bondlens.evidence.indexer import index_evidence, detect_themes


def create_test_messages():
    """Create test messages."""
    return [
        Message(
            message_id="m_001",
            conversation_id="default",
            source_type="csv",
            timestamp=datetime(2025, 5, 21, 22, 13, 5),
            sender_role=SenderRole.TARGET,
            message_type=MessageType.TEXT,
            modality=Modality.TEXT,
            text="今天其实有点想你",
        ),
        Message(
            message_id="m_002",
            conversation_id="default",
            source_type="csv",
            timestamp=datetime(2025, 5, 21, 22, 14, 20),
            sender_role=SenderRole.SELF,
            message_type=MessageType.TEXT,
            modality=Modality.TEXT,
            text="真的吗？我也在想你",
        ),
    ]


def create_test_session():
    """Create test session."""
    return Session(
        session_id="S-20250521-001",
        conversation_id="default",
        start=datetime(2025, 5, 21, 22, 13, 5),
        end=datetime(2025, 5, 21, 22, 14, 20),
        message_count=2,
        self_count=1,
        target_count=1,
        message_ids=["m_001", "m_002"],
    )


def test_index_evidence_basic():
    """Test basic evidence indexing."""
    messages = create_test_messages()
    sessions = [create_test_session()]

    evidence_list = index_evidence(messages, sessions)
    assert len(evidence_list) == 2


def test_evidence_ids_unique():
    """Test that evidence IDs are unique."""
    messages = create_test_messages()
    sessions = [create_test_session()]

    evidence_list = index_evidence(messages, sessions)
    evidence_ids = [e.evidence_id for e in evidence_list]
    assert len(evidence_ids) == len(set(evidence_ids))


def test_detect_themes():
    """Test theme detection."""
    message = Message(
        message_id="m_001",
        conversation_id="default",
        source_type="csv",
        timestamp=datetime(2025, 5, 21, 22, 13, 5),
        sender_role=SenderRole.TARGET,
        message_type=MessageType.TEXT,
        modality=Modality.TEXT,
        text="今天其实有点想你",
    )

    themes = detect_themes(message)
    assert "情感表达" in themes
