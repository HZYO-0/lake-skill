"""WeChat TXT adapter."""

import re
from pathlib import Path
from typing import Any, Generator, Optional

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


# WeChat message pattern: "2025-05-21 22:13:05 张三: 内容"
WECHAT_PATTERN = re.compile(
    r"^(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+(.+?):\s*(.*)$",
    re.DOTALL,
)

# System message patterns
SYSTEM_PATTERNS = [
    re.compile(r"^(.+?)\s+(加入了群聊|退出了群聊|修改了群名称|撤回了一条消息)"),
    re.compile(r"^(你|对方)\s+(撤回了一条消息|邀请.+?加入了群聊)"),
]


class WeChatTXTAdapter(BaseAdapter):
    """Adapter for reading WeChat TXT exports."""

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

    def _is_system_message(self, text: str) -> bool:
        """Check if message is a system message."""
        for pattern in SYSTEM_PATTERNS:
            if pattern.match(text):
                return True
        return False

    def _determine_sender_role(self, sender: str) -> SenderRole:
        """Determine sender role based on name."""
        if not sender:
            return SenderRole.UNKNOWN
        if self.self_name and sender == self.self_name:
            return SenderRole.SELF
        if self.target_name and sender == self.target_name:
            return SenderRole.TARGET
        return SenderRole.UNKNOWN

    def _parse_message(
        self, timestamp_str: str, sender: str, text: str, line_num: int
    ) -> Optional[Message]:
        """Parse a single WeChat message."""
        # Parse timestamp
        try:
            timestamp = date_parser.parse(timestamp_str)
        except Exception:
            self.add_warning(line_num, f"Invalid timestamp: {timestamp_str}")
            return None

        # Determine if system message
        if self._is_system_message(text):
            message_type = MessageType.SYSTEM
            modality = Modality.TEXT
        else:
            message_type = MessageType.TEXT
            modality = Modality.TEXT

        # Determine sender role
        sender_role = self._determine_sender_role(sender)

        return Message(
            message_id=f"txt_{line_num}",
            conversation_id="default",
            source_type="txt",
            timestamp=timestamp,
            sender_role=sender_role,
            message_type=message_type,
            modality=modality,
            text=text,
            raw_text=text,
            source=SourceInfo(file=""),
            quality=QualityInfo(
                parse_confidence=ParseConfidence.HIGH,
                timestamp_confidence=ParseConfidence.HIGH,
            ),
        )

    def read(self, file_path: Path, **kwargs: Any) -> Generator[Message, None, None]:
        """Read messages from WeChat TXT file.

        Args:
            file_path: Path to TXT file

        Yields:
            Message objects
        """
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        current_message: Optional[Message] = None
        current_text_lines: list[str] = []

        for line_num, line in enumerate(lines, 1):
            line = line.rstrip("\n")

            # Check if this is a new message
            match = WECHAT_PATTERN.match(line)
            if match:
                # Save previous message if exists
                if current_message and current_text_lines:
                    current_message.text = "\n".join(current_text_lines)
                    current_message.raw_text = current_message.text
                    yield current_message

                # Parse new message
                timestamp_str, sender, text = match.groups()
                current_message = self._parse_message(
                    timestamp_str, sender, text, line_num
                )
                current_text_lines = [text] if text else []
            else:
                # Continuation of previous message
                if current_message:
                    current_text_lines.append(line)

        # Save last message
        if current_message and current_text_lines:
            current_message.text = "\n".join(current_text_lines)
            current_message.raw_text = current_message.text
            yield current_message
