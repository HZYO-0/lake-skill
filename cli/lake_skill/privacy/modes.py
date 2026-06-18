"""Privacy modes for LakeSkill."""

from enum import Enum

from pydantic import BaseModel


class PrivacyMode(str, Enum):
    """Privacy mode enum."""

    LOCAL_RAW = "local-raw"
    LOCAL_SAFE = "local-safe"
    CLOUD_SAFE = "cloud-safe"
    PUBLISH_SAFE = "publish-safe"


class PrivacyConfig(BaseModel):
    """Privacy configuration for a specific mode."""

    mode: PrivacyMode
    redact_names: bool = False
    redact_contact_info: bool = False
    redact_locations: bool = False
    redact_organizations: bool = False
    redact_financial: bool = False
    redact_ids: bool = False
    coarsen_time: bool = False
    require_synthetic_data: bool = False
    warning_required: bool = False


# Privacy mode configurations
PRIVACY_CONFIGS: dict[PrivacyMode, PrivacyConfig] = {
    PrivacyMode.LOCAL_RAW: PrivacyConfig(
        mode=PrivacyMode.LOCAL_RAW,
        redact_names=False,
        redact_contact_info=False,
        redact_locations=False,
        redact_organizations=False,
        redact_financial=False,
        redact_ids=False,
        coarsen_time=False,
        require_synthetic_data=False,
        warning_required=True,
    ),
    PrivacyMode.LOCAL_SAFE: PrivacyConfig(
        mode=PrivacyMode.LOCAL_SAFE,
        redact_names=False,
        redact_contact_info=True,
        redact_locations=False,
        redact_organizations=False,
        redact_financial=False,
        redact_ids=True,
        coarsen_time=False,
        require_synthetic_data=False,
        warning_required=False,
    ),
    PrivacyMode.CLOUD_SAFE: PrivacyConfig(
        mode=PrivacyMode.CLOUD_SAFE,
        redact_names=True,
        redact_contact_info=True,
        redact_locations=True,
        redact_organizations=True,
        redact_financial=True,
        redact_ids=True,
        coarsen_time=True,
        require_synthetic_data=False,
        warning_required=False,
    ),
    PrivacyMode.PUBLISH_SAFE: PrivacyConfig(
        mode=PrivacyMode.PUBLISH_SAFE,
        redact_names=True,
        redact_contact_info=True,
        redact_locations=True,
        redact_organizations=True,
        redact_financial=True,
        redact_ids=True,
        coarsen_time=True,
        require_synthetic_data=True,
        warning_required=False,
    ),
}


def get_privacy_config(mode: PrivacyMode) -> PrivacyConfig:
    """Get privacy configuration for a mode.

    Args:
        mode: Privacy mode

    Returns:
        Privacy configuration
    """
    return PRIVACY_CONFIGS[mode]


def validate_privacy_mode(mode: str) -> PrivacyMode:
    """Validate and convert string to PrivacyMode.

    Args:
        mode: Privacy mode string

    Returns:
        PrivacyMode enum value

    Raises:
        ValueError: If mode is invalid
    """
    try:
        return PrivacyMode(mode)
    except ValueError:
        valid_modes = [m.value for m in PrivacyMode]
        raise ValueError(f"Invalid privacy mode: {mode}. Valid modes: {valid_modes}")
