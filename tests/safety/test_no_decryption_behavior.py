"""Tests for no decryption behavior."""

import pytest
import tempfile
from pathlib import Path

from bondlens.adapters.wechat_sqlite import WeChatSQLiteAdapter


def test_encrypted_database_error():
    """Test that encrypted database raises appropriate error."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        # Create a fake encrypted database
        db_path = tmp_path / "encrypted.db"
        db_path.write_bytes(b"SQLite format 3\x00" + b"\x00" * 100)

        adapter = WeChatSQLiteAdapter()

        with pytest.raises(Exception) as exc_info:
            list(adapter.read(db_path))

        # Should raise error about unreadable database
        error_msg = str(exc_info.value).lower()
        assert "encrypted" in error_msg or "not readable" in error_msg or "database" in error_msg
