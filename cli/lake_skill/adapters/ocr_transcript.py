"""OCR transcript adapter."""

import csv
from datetime import datetime
from pathlib import Path
from typing import Any, Generator, Optional

from ..jsonl_utils import read_jsonl
from ..schema import (
    MediaInfo,
    Message,
    MessageType,
    Modality,
    ParseConfidence,
    QualityInfo,
    SenderRole,
    SourceInfo,
)
from .base import BaseAdapter


class OCRTranscriptAdapter(BaseAdapter):
    """Adapter for reading OCR transcripts."""

    def __init__(
        self,
        warnings_path: Optional[Path] = None,
        sender_role: SenderRole = SenderRole.TARGET,
        conversation_id: Optional[str] = None,
        source_image: Optional[str] = None,
    ) -> None:
        """Initialize adapter.

        Args:
            warnings_path: Path to write warnings
            sender_role: Role of the speaker
            conversation_id: Conversation ID
            source_image: Source image file name
        """
        super().__init__(warnings_path)
        self.sender_role = sender_role
        self.conversation_id = conversation_id or "default"
        self.source_image = source_image

    def _read_jsonl(self, file_path: Path) -> Generator[Message, None, None]:
        """Read JSONL file."""
        for line_num, data in enumerate(read_jsonl(file_path), 1):
            try:
                # Extract fields
                text = data.get("text", "")
                timestamp_str = data.get("timestamp")
                ocr_confidence = data.get("ocr_confidence")
                data.get("source_image", self.source_image)

                # Parse timestamp
                timestamp = None
                if timestamp_str:
                    try:
                        timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
                    except Exception:
                        pass

                if not timestamp:
                    timestamp = datetime.now()

                message = Message(
                    message_id=data.get("id", f"ocr_{line_num}"),
                    conversation_id=self.conversation_id,
                    source_type="ocr_transcript",
                    timestamp=timestamp,
                    sender_role=self.sender_role,
                    message_type=MessageType.OCR_TRANSCRIPT,
                    modality=Modality.TEXT,
                    text=text,
                    raw_text=text,
                    media=MediaInfo(
                        ocr_confidence=ocr_confidence,
                        ocr_text=text,
                        transcript_source="jsonl",
                    ),
                    source=SourceInfo(file=str(file_path)),
                    quality=QualityInfo(
                        parse_confidence=ParseConfidence.MEDIUM if ocr_confidence and ocr_confidence < 0.80 else ParseConfidence.HIGH,
                        ocr_confidence=ocr_confidence,
                        timestamp_confidence=ParseConfidence.LOW,
                    ),
                )
                yield message

            except Exception as e:
                self.add_warning(line_num, str(e))
                continue

    def _read_csv(self, file_path: Path) -> Generator[Message, None, None]:
        """Read CSV file."""
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for line_num, row in enumerate(reader, 2):
                try:
                    text = row.get("text", "")
                    timestamp_str = row.get("timestamp")
                    ocr_confidence = row.get("ocr_confidence")
                    row.get("source_image", self.source_image)

                    # Parse timestamp
                    timestamp = None
                    if timestamp_str:
                        try:
                            timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
                        except Exception:
                            pass

                    if not timestamp:
                        timestamp = datetime.now()

                    # Parse confidence
                    ocr_conf_val = None
                    if ocr_confidence:
                        try:
                            ocr_conf_val = float(ocr_confidence)
                        except ValueError:
                            pass

                    message = Message(
                        message_id=f"ocr_{line_num}",
                        conversation_id=self.conversation_id,
                        source_type="ocr_transcript",
                        timestamp=timestamp,
                        sender_role=self.sender_role,
                        message_type=MessageType.OCR_TRANSCRIPT,
                        modality=Modality.TEXT,
                        text=text,
                        raw_text=text,
                        media=MediaInfo(
                            ocr_confidence=ocr_conf_val,
                            ocr_text=text,
                            transcript_source="csv",
                        ),
                        source=SourceInfo(file=str(file_path)),
                        quality=QualityInfo(
                            parse_confidence=ParseConfidence.MEDIUM if ocr_conf_val and ocr_conf_val < 0.80 else ParseConfidence.HIGH,
                            ocr_confidence=ocr_conf_val,
                            timestamp_confidence=ParseConfidence.LOW,
                        ),
                    )
                    yield message

                except Exception as e:
                    self.add_warning(line_num, str(e))
                    continue

    def read(self, file_path: Path, **kwargs: Any) -> Generator[Message, None, None]:
        """Read messages from OCR transcript file.

        Args:
            file_path: Path to transcript file

        Yields:
            Message objects
        """
        suffix = file_path.suffix.lower()

        if suffix in (".jsonl", ".json"):
            yield from self._read_jsonl(file_path)
        elif suffix == ".csv":
            yield from self._read_csv(file_path)
        else:
            raise ValueError(f"Unsupported file format: {suffix}")
