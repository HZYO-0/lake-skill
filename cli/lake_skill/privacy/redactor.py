"""Redactor for sensitive information."""

import re

from .modes import PrivacyConfig, PrivacyMode


# Patterns for sensitive information
PATTERNS = {
    # Phone numbers (Chinese)
    "phone": re.compile(r"1[3-9]\d{9}"),
    # ID card (Chinese)
    "id_card": re.compile(r"[1-9]\d{5}(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx]"),
    # Email
    "email": re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"),
    # WeChat ID (alphanumeric, 6-20 chars)
    "wechat_id": re.compile(r"wxid_[a-zA-Z0-9_]{6,20}"),
    # Bank card (16-19 digits)
    "bank_card": re.compile(r"\d{16,19}"),
    # IP address
    "ip_address": re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"),
    # Latitude/Longitude
    "coordinates": re.compile(r"[+-]?\d+\.\d{4,}"),
}

# Replacement markers
REPLACEMENTS = {
    "phone": "[PHONE]",
    "id_card": "[ID_CARD]",
    "email": "[EMAIL]",
    "wechat_id": "[WECHAT_ID]",
    "bank_card": "[BANK_CARD]",
    "ip_address": "[IP]",
    "coordinates": "[COORDINATES]",
    "name": "[NAME]",
    "organization": "[ORG]",
    "location": "[LOCATION]",
    "amount": "[AMOUNT]",
}


class Redactor:
    """Redact sensitive information from text."""

    def __init__(self, config: PrivacyConfig) -> None:
        """Initialize redactor with privacy config.

        Args:
            config: Privacy configuration
        """
        self.config = config

    def redact_text(self, text: str, field_name: str = "text") -> str:
        """Redact sensitive information from text.

        Args:
            text: Text to redact
            field_name: Name of the field being redacted

        Returns:
            Redacted text
        """
        if not text:
            return text

        result = text

        # Always redact high-risk identifiers
        if self.config.redact_ids:
            result = self._redact_pattern(result, "phone")
            result = self._redact_pattern(result, "id_card")
            result = self._redact_pattern(result, "bank_card")

        if self.config.redact_contact_info:
            result = self._redact_pattern(result, "email")
            result = self._redact_pattern(result, "wechat_id")

        if self.config.redact_locations:
            result = self._redact_pattern(result, "ip_address")
            result = self._redact_pattern(result, "coordinates")

        return result

    def _redact_pattern(self, text: str, pattern_name: str) -> str:
        """Redact a specific pattern from text.

        Args:
            text: Text to redact
            pattern_name: Name of the pattern to redact

        Returns:
            Redacted text
        """
        pattern = PATTERNS.get(pattern_name)
        if not pattern:
            return text

        replacement = REPLACEMENTS.get(pattern_name, "[REDACTED]")
        return pattern.sub(replacement, text)

    def redact_message(self, message: dict) -> dict:
        """Redact sensitive information from a message.

        Args:
            message: Message dictionary

        Returns:
            Redacted message dictionary
        """
        import copy
        result = copy.deepcopy(message)

        # Redact text fields
        if "text" in result:
            result["text_redacted"] = self.redact_text(result["text"], "text")

        if "raw_text" in result:
            # Don't redact raw_text, keep original
            pass

        # Redact sender/receiver IDs if needed
        if self.config.redact_names:
            if "sender_id" in result and result["sender_id"]:
                result["sender_id"] = "[SENDER_ID]"

        return result


def create_redactor(mode: PrivacyMode) -> Redactor:
    """Create a redactor for the specified privacy mode.

    Args:
        mode: Privacy mode

    Returns:
        Redactor instance
    """
    from .modes import get_privacy_config
    config = get_privacy_config(mode)
    return Redactor(config)
