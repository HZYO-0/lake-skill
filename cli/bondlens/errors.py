"""Error handling for WRI."""


class BondLensError(Exception):
    """Base BondLens error."""

    pass


class ConfigError(BondLensError):
    """Configuration error."""

    pass


class SchemaError(BondLensError):
    """Schema validation error."""

    pass


class AdapterError(BondLensError):
    """Adapter error."""

    pass


class PrivacyError(BondLensError):
    """Privacy violation error."""

    pass


class EncryptedDatabaseError(AdapterError):
    """Encrypted database error."""

    def __init__(self, db_path: str) -> None:
        super().__init__(
            f"Database '{db_path}' is encrypted or not readable. "
            "BondLens does not decrypt databases. Please provide a readable plaintext SQLite database."
        )


class ParseError(AdapterError):
    """Parse error."""

    pass


class ValidationError(SchemaError):
    """Validation error."""

    pass
