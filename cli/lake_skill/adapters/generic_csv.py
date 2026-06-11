"""Generic CSV adapter."""

import csv
from datetime import datetime
from pathlib import Path
from typing import Any, Generator, Optional, Sequence

from dateutil import parser as date_parser

from ..schema import (
    Message,
    MessageType,
    Modality,
    ParseConfidence,
    QualityInfo,
    SenderRole,
    SourceInfo,
)
from .base import BaseAdapter


# Common column name mappings
COLUMN_MAPPINGS = {
    # Chinese names
    "时间": "timestamp",
    "日期": "timestamp",
    "发送者": "sender",
    "发送人": "sender",
    "发送方": "sender",
    "接收者": "receiver",
    "接收人": "receiver",
    "接收方": "receiver",
    "内容": "text",
    "消息": "text",
    "消息内容": "text",
    "类型": "message_type",
    "消息类型": "message_type",
    # English names
    "timestamp": "timestamp",
    "time": "timestamp",
    "date": "timestamp",
    "sender": "sender",
    "from": "sender",
    "receiver": "receiver",
    "to": "receiver",
    "content": "text",
    "text": "text",
    "message": "text",
    "msg": "text",
    "type": "message_type",
}


class GenericCSVAdapter(BaseAdapter):
    """Adapter for reading generic CSV files."""

    def __init__(
        self,
        warnings_path: Optional[Path] = None,
        self_name: Optional[str] = None,
        target_name: Optional[str] = None,
    ) -> None:
        """Initialize adapter.

        Args:
            warnings_path: Path to write warnings
            self_name: Name of the self user
            target_name: Name of the target user
        """
        super().__init__(warnings_path)
        self.self_name = self_name
        self.target_name = target_name

    def _map_columns(self, fieldnames: Sequence[str]) -> dict[str, str]:
        """Map CSV columns to standard field names."""
        mapping = {}
        for field in fieldnames:
            field_lower = field.lower().strip()
            if field_lower in COLUMN_MAPPINGS:
                mapping[field] = COLUMN_MAPPINGS[field_lower]
        return mapping

    def _parse_timestamp(self, value: str) -> Optional[datetime]:
        """Parse timestamp string."""
        if not value or not value.strip():
            return None
        try:
            return date_parser.parse(value)
        except Exception:
            return None

    def _determine_sender_role(
        self, sender: str, receiver: Optional[str] = None
    ) -> SenderRole:
        """Determine sender role based on names."""
        if not sender:
            return SenderRole.UNKNOWN

        if self.self_name and sender == self.self_name:
            return SenderRole.SELF
        if self.target_name and sender == self.target_name:
            return SenderRole.TARGET

        # If we have receiver info and it matches self, sender is target
        if self.self_name and receiver == self.self_name:
            return SenderRole.TARGET
        if self.target_name and receiver == self.target_name:
            return SenderRole.SELF

        return SenderRole.UNKNOWN

    def read(self, file_path: Path, **kwargs: Any) -> Generator[Message, None, None]:
        """Read messages from CSV file.

        Args:
            file_path: Path to CSV file

        Yields:
            Message objects
        """
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            if not reader.fieldnames:
                self.add_warning(0, "No headers found in CSV")
                return

            column_map = self._map_columns(reader.fieldnames)
            # Create reverse mapping: standard_name -> original_name
            reverse_map = {v: k for k, v in column_map.items()}

            for line_num, row in enumerate(reader, 2):
                try:
                    # Extract fields using reverse mapping
                    timestamp_str = row.get(reverse_map.get("timestamp", ""), "")
                    sender = row.get(reverse_map.get("sender", ""), "")
                    receiver = row.get(reverse_map.get("receiver", ""), "")
                    text = row.get(reverse_map.get("text", ""), "")
                    row.get(reverse_map.get("message_type", ""), "text")

                    # Parse timestamp
                    timestamp = self._parse_timestamp(timestamp_str)
                    if not timestamp:
                        self.add_warning(
                            line_num,
                            f"Invalid timestamp: {timestamp_str}",
                            str(row),
                        )
                        continue

                    # Determine sender role
                    sender_role = self._determine_sender_role(sender, receiver)

                    # Create message
                    message = Message(
                        message_id=f"csv_{line_num}",
                        conversation_id="default",
                        source_type="csv",
                        timestamp=timestamp,
                        sender_role=sender_role,
                        message_type=MessageType.TEXT,
                        modality=Modality.TEXT,
                        text=text,
                        raw_text=text,
                        source=SourceInfo(file=str(file_path)),
                        quality=QualityInfo(
                            parse_confidence=ParseConfidence.HIGH,
                            timestamp_confidence=ParseConfidence.HIGH,
                        ),
                    )
                    yield message

                except Exception as e:
                    self.add_warning(line_num, str(e), str(row))
                    continue
