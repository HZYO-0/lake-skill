"""Configuration management for BondLens."""

from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, Field


class PrivacyConfig(BaseModel):
    """Privacy configuration."""

    default_privacy_mode: str = "cloud-safe"
    raw_upload_allowed: bool = False
    upload_policy: str = "digest_and_evidence_only"


class SegmentationConfig(BaseModel):
    """Segmentation configuration."""

    default_time_gap_hours: int = 6
    long_gap_hours: int = 24
    detect_episode_types: list[str] = Field(
        default_factory=lambda: [
            "ambiguous",
            "reassurance",
            "relationship_pressure",
            "conflict",
            "repair",
            "coldness",
            "reconnection",
            "breakup",
            "boundary",
        ]
    )


class AnalysisConfig(BaseModel):
    """Analysis configuration."""

    evidence_required: bool = True
    minimum_evidence_for_medium_confidence: int = 3
    require_counterevidence: bool = True
    require_alternative_explanations: bool = True
    allow_clinical_diagnosis: bool = False
    allow_personality_disorder_labels: bool = False
    allow_manipulation_tactics: bool = False
    allow_symbolic_astrology_tarot: bool = False


class EvidenceConfig(BaseModel):
    """Evidence configuration."""

    quote_max_chars: int = 280
    low_asr_confidence_threshold: float = 0.75
    low_ocr_confidence_threshold: float = 0.80
    high_confidence_requires_counterevidence_review: bool = True


class BondLensConfig(BaseModel):
    """Main BondLens configuration."""

    project_name: str = "bondlens"
    default_relationship_type: str = "ambiguous"
    timezone: str = "Asia/Shanghai"
    privacy: PrivacyConfig = Field(default_factory=PrivacyConfig)
    segmentation: SegmentationConfig = Field(default_factory=SegmentationConfig)
    analysis: AnalysisConfig = Field(default_factory=AnalysisConfig)
    evidence: EvidenceConfig = Field(default_factory=EvidenceConfig)


def load_config(config_path: Optional[Path] = None) -> BondLensConfig:
    """Load configuration from file or use defaults."""
    if config_path is None:
        config_path = Path("config.yaml")

    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if data:
            return BondLensConfig(**data)

    return BondLensConfig()


def save_config(config: BondLensConfig, config_path: Path) -> None:
    """Save configuration to file."""
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.dump(config.model_dump(), f, default_flow_style=False, allow_unicode=True)
