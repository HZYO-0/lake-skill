"""Error handling for WRI."""


class LakeSkillError(Exception):
    """Base LakeSkill error."""

    pass


class ConfigError(LakeSkillError):
    """Configuration error."""

    pass


class SchemaError(LakeSkillError):
    """Schema validation error."""

    pass


class AdapterError(LakeSkillError):
    """Adapter error."""

    pass


class PrivacyError(LakeSkillError):
    """Privacy violation error."""

    pass


class EncryptedDatabaseError(AdapterError):
    """Encrypted database error."""

    def __init__(self, db_path: str) -> None:
        super().__init__(
            f"Database '{db_path}' is encrypted or not readable. "
            "LakeSkill does not decrypt databases. Please provide a readable plaintext SQLite database."
        )


class ParseError(AdapterError):
    """Parse error."""

    pass


class ValidationError(SchemaError):
    """Validation error."""

    pass
