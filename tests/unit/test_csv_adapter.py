"""Tests for CSV adapter."""

import json
import tempfile
from pathlib import Path

from lake_skill.adapters.generic_csv import GenericCSVAdapter


def test_csv_adapter_basic():
    """Test basic CSV adapter functionality."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(
            "timestamp,sender,receiver,content\n2025-05-21 22:13:05,张三,我,今天其实有点想你\n2025-05-21 22:14:20,我,张三,真的吗？我也在想你\n",
            encoding="utf-8",
        )

        output_file = tmp_path / "output.jsonl"
        adapter = GenericCSVAdapter(self_name="我", target_name="张三")

        count = adapter.process(csv_file, output_file)
        assert count == 2
        assert output_file.exists()


def test_csv_adapter_sender_role():
    """Test sender role detection."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(
            "timestamp,sender,receiver,content\n2025-05-21 22:13:05,张三,我,今天其实有点想你\n2025-05-21 22:14:20,我,张三,真的吗？我也在想你\n",
            encoding="utf-8",
        )

        output_file = tmp_path / "output.jsonl"
        adapter = GenericCSVAdapter(self_name="我", target_name="张三")
        adapter.process(csv_file, output_file)

        with open(output_file, "r", encoding="utf-8") as f:
            messages = [json.loads(line) for line in f]

        assert messages[0]["sender_role"] == "target"
        assert messages[1]["sender_role"] == "self"


def test_csv_adapter_text_content():
    """Test text content extraction."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(
            "timestamp,sender,receiver,content\n2025-05-21 22:13:05,张三,我,今天其实有点想你\n2025-05-21 22:14:20,我,张三,真的吗？我也在想你\n",
            encoding="utf-8",
        )

        output_file = tmp_path / "output.jsonl"
        adapter = GenericCSVAdapter(self_name="我", target_name="张三")
        adapter.process(csv_file, output_file)

        with open(output_file, "r", encoding="utf-8") as f:
            messages = [json.loads(line) for line in f]

        assert messages[0]["text"] == "今天其实有点想你"
        assert messages[1]["text"] == "真的吗？我也在想你"
