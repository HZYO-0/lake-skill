"""Knowledge base schema for WRI."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .. import __version__


class KBObservation(BaseModel):
    """Knowledge base observation."""

    id: str
    type: str  # new, reinforced, revised, counterevidence
    content: str
    evidence_ids: list[str] = Field(default_factory=list)
    confidence: str = "medium"
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class KBProfile(BaseModel):
    """Target profile in knowledge base."""

    name: Optional[str] = None
    relationship_type: str = "ambiguous"
    communication_style: Optional[str] = None
    emotional_patterns: list[str] = Field(default_factory=list)
    attachment_signals: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class KBMetadata(BaseModel):
    """Knowledge base metadata."""

    version: str = __version__
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    message_count: int = 0
    session_count: int = 0
    evidence_count: int = 0
    privacy_mode: str = "cloud-safe"


class KnowledgeBase(BaseModel):
    """Complete knowledge base structure."""

    metadata: KBMetadata = Field(default_factory=KBMetadata)
    profile: KBProfile = Field(default_factory=KBProfile)
    observations: list[KBObservation] = Field(default_factory=list)
    unresolved_questions: list[str] = Field(default_factory=list)
    update_log: list[dict] = Field(default_factory=list)


class KBPatch(BaseModel):
    """Knowledge base patch."""

    patch_id: str
    created_at: datetime = Field(default_factory=datetime.now)
    new_observations: list[KBObservation] = Field(default_factory=list)
    reinforced_observations: list[KBObservation] = Field(default_factory=list)
    revised_observations: list[KBObservation] = Field(default_factory=list)
    counterevidence: list[KBObservation] = Field(default_factory=list)
    confidence_updates: list[dict] = Field(default_factory=list)
    unresolved_questions: list[str] = Field(default_factory=list)
    summary: str = ""
