"""Data schemas for WRI."""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class SenderRole(str, Enum):
    """Sender role enum."""

    SELF = "self"
    TARGET = "target"
    OTHER = "other"
    UNKNOWN = "unknown"


class MessageType(str, Enum):
    """Message type enum."""

    TEXT = "text"
    IMAGE = "image"
    VOICE = "voice"
    VIDEO = "video"
    FILE = "file"
    LINK = "link"
    LOCATION = "location"
    SYSTEM = "system"
    VOICE_TRANSCRIPT = "voice_transcript"
    OCR_TRANSCRIPT = "ocr_transcript"


class Modality(str, Enum):
    """Modality enum."""

    TEXT = "text"
    AUDIO = "audio"
    IMAGE = "image"
    VIDEO = "video"
    MULTIMEDIA = "multimedia"


class ParseConfidence(str, Enum):
    """Parse confidence level."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class MediaInfo(BaseModel):
    """Media information."""

    file_name: Optional[str] = None
    duration_sec: Optional[float] = None
    ocr_text: Optional[str] = None
    asr_confidence: Optional[float] = None
    ocr_confidence: Optional[float] = None
    transcript_source: Optional[str] = None
    source_audio: Optional[str] = None


class ConversationContext(BaseModel):
    """Conversation context."""

    is_group: bool = False
    relationship_type: Optional[str] = None
    phase_hint: Optional[str] = None


class SourceInfo(BaseModel):
    """Source information."""

    file: Optional[str] = None
    table: Optional[str] = None
    row_id: Optional[int] = None


class QualityInfo(BaseModel):
    """Quality information."""

    parse_confidence: ParseConfidence = ParseConfidence.HIGH
    asr_confidence: Optional[float] = None
    ocr_confidence: Optional[float] = None
    timestamp_confidence: ParseConfidence = ParseConfidence.HIGH
    notes: list[str] = Field(default_factory=list)


class Message(BaseModel):
    """Standard message schema."""

    message_id: str
    conversation_id: str
    source_app: str = "wechat"
    source_type: str
    timestamp: datetime
    sender_id: Optional[str] = None
    sender_role: SenderRole
    receiver_role: SenderRole = SenderRole.SELF
    message_type: MessageType
    modality: Modality
    text: Optional[str] = None
    text_redacted: Optional[str] = None
    raw_text: Optional[str] = None
    media: MediaInfo = Field(default_factory=MediaInfo)
    conversation_context: ConversationContext = Field(default_factory=ConversationContext)
    source: SourceInfo = Field(default_factory=SourceInfo)
    quality: QualityInfo = Field(default_factory=QualityInfo)
    hash: Optional[str] = None


class Evidence(BaseModel):
    """Evidence schema."""

    evidence_id: str
    session_id: str
    message_ids: list[str]
    source_app: str = "wechat"
    source_type: str
    message_type: str
    speaker: SenderRole
    quote: str
    quote_redacted: Optional[str] = None
    asr_confidence: Optional[float] = None
    ocr_confidence: Optional[float] = None
    theme: list[str] = Field(default_factory=list)
    supports: list[str] = Field(default_factory=list)
    confidence: str = "medium"
    alternative_explanations: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)


class Session(BaseModel):
    """Session schema."""

    session_id: str
    conversation_id: str
    start: datetime
    end: datetime
    topic: Optional[str] = None
    message_count: int = 0
    self_count: int = 0
    target_count: int = 0
    dominant_emotion: Optional[str] = None
    episode_type: list[str] = Field(default_factory=list)
    risk_level: Optional[str] = None
    message_ids: list[str] = Field(default_factory=list)


class WorkMode(str, Enum):
    """Working mode for analysis."""

    SUPPORT = "support"
    PRACTICAL = "practical"
    REPAIR = "repair"
    AUTO = "auto"


class IntakeCard(BaseModel):
    """Machine-readable intake configuration."""

    relationship_type: str = "ambiguous"
    status: str = "unknown"
    self_name: str = ""
    target_name: str = ""
    duration: str = ""
    goal: str = ""
    data_source: str = ""
    privacy_mode: str = "cloud-safe"
    output_preference: str = "action_card_first"
    work_mode: WorkMode = WorkMode.AUTO
    scene_summary: str = ""
    created_at: datetime = Field(default_factory=datetime.now)
    version: str = "4.2.0"
