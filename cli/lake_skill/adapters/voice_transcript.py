"""Voice transcript adapter."""

import csv
import re
from datetime import datetime, timedelta
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


# SRT timestamp pattern: 00:00:00,000 --> 00:00:00,000
SRT_TIMESTAMP_PATTERN = re.compile(
    r"(\d{2}:\d{2}:\d{2}[,\.]\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}[,\.]\d{3})"
)

# VTT timestamp pattern: 00:00:00.000 --> 00:00:00.000
VTT_TIMESTAMP_PATTERN = re.compile(
    r"(\d{2}:\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}\.\d{3})"
)


def parse_srt_timestamp(timestamp_str: str) -> timedelta:
    """Parse SRT timestamp to timedelta."""
    # Replace comma with dot
    timestamp_str = timestamp_str.replace(",", ".")
    hours, minutes, seconds = timestamp_str.split(":")
    secs, millis = seconds.split(".")
    return timedelta(
        hours=int(hours),
        minutes=int(minutes),
        seconds=int(secs),
        milliseconds=int(millis),
    )


def parse_vtt_timestamp(timestamp_str: str) -> timedelta:
    """Parse VTT timestamp to timedelta."""
    hours, minutes, seconds = timestamp_str.split(":")
    secs, millis = seconds.split(".")
    return timedelta(
        hours=int(hours),
        minutes=int(minutes),
        seconds=int(secs),
        milliseconds=int(millis),
    )


class VoiceTranscriptAdapter(BaseAdapter):
    """Adapter for reading voice transcripts."""

    def __init__(
        self,
        warnings_path: Optional[Path] = None,
        sender_role: SenderRole = SenderRole.TARGET,
        conversation_id: Optional[str] = None,
        base_timestamp: Optional[datetime] = None,
        source_audio: Optional[str] = None,
    ) -> None:
        """Initialize adapter.

        Args:
            warnings_path: Path to write warnings
            sender_role: Role of the speaker
            conversation_id: Conversation ID
            base_timestamp: Base timestamp for relative timestamps
            source_audio: Source audio file name
        """
        super().__init__(warnings_path)
        self.sender_role = sender_role
        self.conversation_id = conversation_id or "default"
        self.base_timestamp = base_timestamp
        self.source_audio = source_audio

    def _read_srt(self, file_path: Path) -> Generator[Message, None, None]:
        """Read SRT file."""
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        current_index: Optional[int] = None
        current_start: Optional[timedelta] = None
        current_end: Optional[timedelta] = None
        current_text_lines: list[str] = []

        def _flush_current():
            """Flush current accumulated data as a message."""
            nonlocal current_index, current_start, current_end, current_text_lines
            if current_index is not None and current_text_lines:
                text = " ".join(current_text_lines)
                duration = (current_end - current_start).total_seconds() if current_end and current_start else None

                timestamp = self.base_timestamp
                if timestamp and current_start:
                    timestamp = timestamp + current_start

                message = Message(
                    message_id=f"srt_{current_index}",
                    conversation_id=self.conversation_id,
                    source_type="voice_transcript",
                    timestamp=timestamp or datetime.now(),
                    sender_role=self.sender_role,
                    message_type=MessageType.VOICE_TRANSCRIPT,
                    modality=Modality.AUDIO,
                    text=text,
                    raw_text=text,
                    media=MediaInfo(
                        duration_sec=duration,
                        asr_confidence=0.9,
                        transcript_source="srt",
                        source_audio=self.source_audio,
                    ),
                    source=SourceInfo(file=str(file_path)),
                    quality=QualityInfo(
                        parse_confidence=ParseConfidence.MEDIUM,
                        asr_confidence=0.9,
                        timestamp_confidence=ParseConfidence.MEDIUM,
                    ),
                )
                return message

            # Reset
            current_index = None
            current_start = None
            current_end = None
            current_text_lines = []
            return None

        for line_num, line in enumerate(lines, 1):
            line = line.strip()

            # Skip empty lines
            if not line:
                msg = _flush_current()
                if msg:
                    yield msg
                continue

            # Try to parse as index
            if current_index is None:
                try:
                    current_index = int(line)
                    continue
                except ValueError:
                    pass

            # Try to parse as timestamp
            if current_start is None:
                match = SRT_TIMESTAMP_PATTERN.match(line)
                if match:
                    current_start = parse_srt_timestamp(match.group(1))
                    current_end = parse_srt_timestamp(match.group(2))
                    continue

            # Otherwise, it's text
            current_text_lines.append(line)

        # Flush last entry
        msg = _flush_current()
        if msg:
            yield msg

    def _read_vtt(self, file_path: Path) -> Generator[Message, None, None]:
        """Read VTT file."""
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Skip VTT header
        start_idx = 0
        for i, line in enumerate(lines):
            if line.strip().startswith("WEBVTT"):
                start_idx = i + 1
                break

        current_start: Optional[timedelta] = None
        current_end: Optional[timedelta] = None
        current_text_lines: list[str] = []
        msg_count = 0

        for line_num, line in enumerate(lines[start_idx:], start_idx + 1):
            line = line.strip()

            if not line:
                if current_text_lines:
                    # Create message
                    text = " ".join(current_text_lines)
                    duration = (current_end - current_start).total_seconds() if current_end and current_start else None

                    timestamp = self.base_timestamp
                    if timestamp and current_start:
                        timestamp = timestamp + current_start

                    msg_count += 1
                    message = Message(
                        message_id=f"vtt_{msg_count}",
                        conversation_id=self.conversation_id,
                        source_type="voice_transcript",
                        timestamp=timestamp or datetime.now(),
                        sender_role=self.sender_role,
                        message_type=MessageType.VOICE_TRANSCRIPT,
                        modality=Modality.AUDIO,
                        text=text,
                        raw_text=text,
                        media=MediaInfo(
                            duration_sec=duration,
                            asr_confidence=0.9,
                            transcript_source="vtt",
                            source_audio=self.source_audio,
                        ),
                        source=SourceInfo(file=str(file_path)),
                        quality=QualityInfo(
                            parse_confidence=ParseConfidence.MEDIUM,
                            asr_confidence=0.9,
                            timestamp_confidence=ParseConfidence.MEDIUM,
                        ),
                    )
                    yield message

                    current_start = None
                    current_end = None
                    current_text_lines = []
                continue

            # Try to parse as timestamp
            match = VTT_TIMESTAMP_PATTERN.match(line)
            if match:
                current_start = parse_vtt_timestamp(match.group(1))
                current_end = parse_vtt_timestamp(match.group(2))
                continue

            # Otherwise, it's text
            current_text_lines.append(line)

    def _read_jsonl(self, file_path: Path) -> Generator[Message, None, None]:
        """Read JSONL file."""
        for line_num, data in enumerate(read_jsonl(file_path), 1):
            try:
                # Extract fields
                text = data.get("text", "")
                timestamp_str = data.get("timestamp")
                asr_confidence = data.get("asr_confidence")
                duration = data.get("duration_sec")
                source_audio = data.get("source_audio", self.source_audio)

                # Parse timestamp
                timestamp = None
                if timestamp_str:
                    try:
                        timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
                    except Exception:
                        pass

                if not timestamp:
                    timestamp = self.base_timestamp or datetime.now()

                message = Message(
                    message_id=data.get("id", f"jsonl_{line_num}"),
                    conversation_id=self.conversation_id,
                    source_type="voice_transcript",
                    timestamp=timestamp,
                    sender_role=self.sender_role,
                    message_type=MessageType.VOICE_TRANSCRIPT,
                    modality=Modality.AUDIO,
                    text=text,
                    raw_text=text,
                    media=MediaInfo(
                        duration_sec=duration,
                        asr_confidence=asr_confidence,
                        transcript_source="jsonl",
                        source_audio=source_audio,
                    ),
                    source=SourceInfo(file=str(file_path)),
                    quality=QualityInfo(
                        parse_confidence=ParseConfidence.MEDIUM if asr_confidence and asr_confidence < 0.75 else ParseConfidence.HIGH,
                        asr_confidence=asr_confidence,
                        timestamp_confidence=ParseConfidence.MEDIUM,
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
                    asr_confidence = row.get("asr_confidence")
                    duration = row.get("duration_sec")
                    source_audio = row.get("source_audio", self.source_audio)

                    # Parse timestamp
                    timestamp = None
                    if timestamp_str:
                        try:
                            timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
                        except Exception:
                            pass

                    if not timestamp:
                        timestamp = self.base_timestamp or datetime.now()

                    # Parse confidence
                    asr_conf_val = None
                    if asr_confidence:
                        try:
                            asr_conf_val = float(asr_confidence)
                        except ValueError:
                            pass

                    # Parse duration
                    duration_val = None
                    if duration:
                        try:
                            duration_val = float(duration)
                        except ValueError:
                            pass

                    message = Message(
                        message_id=f"csv_{line_num}",
                        conversation_id=self.conversation_id,
                        source_type="voice_transcript",
                        timestamp=timestamp,
                        sender_role=self.sender_role,
                        message_type=MessageType.VOICE_TRANSCRIPT,
                        modality=Modality.AUDIO,
                        text=text,
                        raw_text=text,
                        media=MediaInfo(
                            duration_sec=duration_val,
                            asr_confidence=asr_conf_val,
                            transcript_source="csv",
                            source_audio=source_audio,
                        ),
                        source=SourceInfo(file=str(file_path)),
                        quality=QualityInfo(
                            parse_confidence=ParseConfidence.MEDIUM if asr_conf_val and asr_conf_val < 0.75 else ParseConfidence.HIGH,
                            asr_confidence=asr_conf_val,
                            timestamp_confidence=ParseConfidence.MEDIUM,
                        ),
                    )
                    yield message

                except Exception as e:
                    self.add_warning(line_num, str(e))
                    continue

    def read(self, file_path: Path, **kwargs: Any) -> Generator[Message, None, None]:
        """Read messages from voice transcript file.

        Args:
            file_path: Path to transcript file

        Yields:
            Message objects
        """
        suffix = file_path.suffix.lower()

        if suffix == ".srt":
            yield from self._read_srt(file_path)
        elif suffix == ".vtt":
            yield from self._read_vtt(file_path)
        elif suffix in (".jsonl", ".json"):
            yield from self._read_jsonl(file_path)
        elif suffix == ".csv":
            yield from self._read_csv(file_path)
        else:
            raise ValueError(f"Unsupported file format: {suffix}")
