"""Deterministic hashing for WRI."""

import hashlib
from datetime import datetime
from typing import Optional


def generate_message_hash(
    timestamp: datetime,
    sender_id: Optional[str],
    text: Optional[str],
    conversation_id: Optional[str] = None,
) -> str:
    """Generate deterministic hash for a message.

    Args:
        timestamp: Message timestamp
        sender_id: Sender ID
        text: Message text
        conversation_id: Conversation ID

    Returns:
        SHA256 hash string
    """
    # Create deterministic string
    parts = [
        timestamp.isoformat(),
        sender_id or "",
        text or "",
        conversation_id or "",
    ]
    content = "|".join(parts)

    # Generate hash
    return f"sha256:{hashlib.sha256(content.encode('utf-8')).hexdigest()}"


def generate_evidence_id(
    date: datetime,
    sequence: int,
    prefix: str = "E",
) -> str:
    """Generate evidence ID.

    Args:
        date: Date for the evidence
        sequence: Sequence number
        prefix: ID prefix

    Returns:
        Evidence ID string
    """
    date_str = date.strftime("%Y%m%d")
    return f"{prefix}-{date_str}-{sequence:03d}"


def generate_session_id(
    date: datetime,
    sequence: int,
    prefix: str = "S",
) -> str:
    """Generate session ID.

    Args:
        date: Date for the session
        sequence: Sequence number

    Returns:
        Session ID string
    """
    date_str = date.strftime("%Y%m%d")
    return f"{prefix}-{date_str}-{sequence:03d}"
