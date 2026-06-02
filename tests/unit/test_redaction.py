"""Tests for redaction."""

from cli.bondlens.privacy.modes import PrivacyMode
from cli.bondlens.privacy.redactor import create_redactor


def test_redact_phone_number():
    """Test phone number redaction."""
    redactor = create_redactor(PrivacyMode.CLOUD_SAFE)
    text = "我的手机号是13812345678"
    result = redactor.redact_text(text)
    assert "[PHONE]" in result
    assert "13812345678" not in result


def test_redact_email():
    """Test email redaction."""
    redactor = create_redactor(PrivacyMode.CLOUD_SAFE)
    text = "我的邮箱是test@example.com"
    result = redactor.redact_text(text)
    assert "[EMAIL]" in result
    assert "test@example.com" not in result


def test_redact_wechat_id():
    """Test WeChat ID redaction."""
    redactor = create_redactor(PrivacyMode.CLOUD_SAFE)
    text = "我的微信号是wxid_abc123def456"
    result = redactor.redact_text(text)
    assert "[WECHAT_ID]" in result
    assert "wxid_abc123def456" not in result


def test_local_raw_no_redaction():
    """Test that local-raw mode does not redact."""
    redactor = create_redactor(PrivacyMode.LOCAL_RAW)
    text = "我的手机号是13812345678"
    result = redactor.redact_text(text)
    assert result == text


def test_redact_message():
    """Test message redaction."""
    redactor = create_redactor(PrivacyMode.CLOUD_SAFE)
    message = {
        "message_id": "m_001",
        "text": "我的手机号是13812345678",
        "sender_id": "wxid_target",
    }
    result = redactor.redact_message(message)
    assert "[PHONE]" in result["text_redacted"]
    assert result["sender_id"] == "[SENDER_ID]"
