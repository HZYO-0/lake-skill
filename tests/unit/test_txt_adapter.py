"""Tests for TXT adapter."""

import json
import tempfile
from pathlib import Path

from lake_skill.adapters.wechat_txt import WeChatTXTAdapter


def test_txt_adapter_basic():
    """Test basic TXT adapter functionality."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        txt_file = tmp_path / "test.txt"
        txt_file.write_text(
            "2025-05-21 22:13:05 张三: 今天其实有点想你\n2025-05-21 22:14:20 我: 真的吗？我也在想你\n",
            encoding="utf-8",
        )

        output_file = tmp_path / "output.jsonl"
        adapter = WeChatTXTAdapter(self_name="我", target_name="张三")

        count = adapter.process(txt_file, output_file)
        assert count == 2
        assert output_file.exists()


def test_txt_adapter_sender_role():
    """Test sender role detection."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        txt_file = tmp_path / "test.txt"
        txt_file.write_text(
            "2025-05-21 22:13:05 张三: 今天其实有点想你\n2025-05-21 22:14:20 我: 真的吗？我也在想你\n",
            encoding="utf-8",
        )

        output_file = tmp_path / "output.jsonl"
        adapter = WeChatTXTAdapter(self_name="我", target_name="张三")
        adapter.process(txt_file, output_file)

        with open(output_file, "r", encoding="utf-8") as f:
            messages = [json.loads(line) for line in f]

        assert messages[0]["sender_role"] == "target"
        assert messages[1]["sender_role"] == "self"


def test_txt_adapter_text_content():
    """Test text content extraction."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        txt_file = tmp_path / "test.txt"
        txt_file.write_text(
            "2025-05-21 22:13:05 张三: 今天其实有点想你\n2025-05-21 22:14:20 我: 真的吗？我也在想你\n",
            encoding="utf-8",
        )

        output_file = tmp_path / "output.jsonl"
        adapter = WeChatTXTAdapter(self_name="我", target_name="张三")
        adapter.process(txt_file, output_file)

        with open(output_file, "r", encoding="utf-8") as f:
            messages = [json.loads(line) for line in f]

        assert messages[0]["text"] == "今天其实有点想你"
        assert messages[1]["text"] == "真的吗？我也在想你"
