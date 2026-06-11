"""Tests for lake-skill intake and doctor CLI commands."""

import pytest


def _check_cli_deps() -> None:
    try:
        import typer  # noqa: F401
        import pydantic  # noqa: F401
    except ImportError as e:
        pytest.skip(f"CLI dependencies not installed: {e}")


@pytest.fixture()
def cli_runner():
    _check_cli_deps()
    from typer.testing import CliRunner
    from lake_skill.cli import app
    return CliRunner(), app


def test_intake_generates_yaml_and_md(cli_runner, tmp_path):
    """lake-skill intake creates both YAML and MD files."""
    runner, app = cli_runner
    result = runner.invoke(app, [
        "intake",
        "--out", str(tmp_path),
        "--type", "暧昧",
        "--status", "冷淡期",
        "--self-name", "我",
        "--target-name", "她",
        "--work-mode", "practical",
    ])
    assert result.exit_code == 0
    assert (tmp_path / "lakeskill_intake.yaml").exists()
    assert (tmp_path / "lakeskill_intake.md").exists()


def test_intake_invalid_work_mode_fails(cli_runner, tmp_path):
    """lake-skill intake rejects invalid work mode."""
    runner, app = cli_runner
    result = runner.invoke(app, [
        "intake",
        "--out", str(tmp_path),
        "--work-mode", "invalid_mode",
    ])
    assert result.exit_code == 1


def test_intake_yaml_loads_back(cli_runner, tmp_path):
    """Generated YAML can be loaded back as IntakeCard."""
    runner, app = cli_runner
    result = runner.invoke(app, [
        "intake",
        "--out", str(tmp_path),
        "--type", "暧昧",
        "--status", "冷淡期",
        "--work-mode", "repair",
    ])
    assert result.exit_code == 0

    from lake_skill.intake_io import load_intake_yaml
    from lake_skill.schema import IntakeCard, WorkMode

    card = load_intake_yaml(tmp_path / "lakeskill_intake.yaml")
    assert isinstance(card, IntakeCard)
    assert card.relationship_type == "暧昧"
    assert card.status == "冷淡期"
    assert card.work_mode == WorkMode.REPAIR


def test_intake_md_contains_work_mode(cli_runner, tmp_path):
    """Generated MD contains work mode field."""
    runner, app = cli_runner
    result = runner.invoke(app, [
        "intake",
        "--out", str(tmp_path),
        "--work-mode", "support",
    ])
    assert result.exit_code == 0

    content = (tmp_path / "lakeskill_intake.md").read_text(encoding="utf-8")
    assert "support" in content


def test_doctor_with_sufficient_data(cli_runner, tmp_path):
    """lake-skill doctor reports OK for 100+ message dataset."""
    runner, app = cli_runner

    from lake_skill.schema import Message, SenderRole, MessageType, Modality
    from datetime import datetime, timedelta
    from lake_skill.jsonl_utils import write_jsonl_models

    messages = []
    for i in range(120):
        role = SenderRole.SELF if i % 2 == 0 else SenderRole.TARGET
        messages.append(Message(
            message_id=f"msg-{i}",
            conversation_id="test-conv",
            source_type="csv",
            timestamp=datetime(2026, 1, 1) + timedelta(hours=i),
            sender_role=role,
            message_type=MessageType.TEXT,
            modality=Modality.TEXT,
            text=f"Message {i}",
        ))

    messages_path = tmp_path / "messages.jsonl"
    write_jsonl_models(messages_path, messages)

    result = runner.invoke(app, [
        "doctor",
        "--messages", str(messages_path),
        "--out", str(tmp_path),
    ])
    assert result.exit_code == 0
    assert (tmp_path / "data_readiness.md").exists()


def test_doctor_with_sparse_data(cli_runner, tmp_path):
    """lake-skill doctor warns on < 30 messages."""
    runner, app = cli_runner

    from lake_skill.schema import Message, SenderRole, MessageType, Modality
    from datetime import datetime, timedelta
    from lake_skill.jsonl_utils import write_jsonl_models

    messages = []
    for i in range(10):
        role = SenderRole.SELF if i % 2 == 0 else SenderRole.TARGET
        messages.append(Message(
            message_id=f"msg-{i}",
            conversation_id="test-conv",
            source_type="csv",
            timestamp=datetime(2026, 1, 1) + timedelta(hours=i),
            sender_role=role,
            message_type=MessageType.TEXT,
            modality=Modality.TEXT,
            text=f"Message {i}",
        ))

    messages_path = tmp_path / "messages.jsonl"
    write_jsonl_models(messages_path, messages)

    result = runner.invoke(app, [
        "doctor",
        "--messages", str(messages_path),
        "--out", str(tmp_path),
    ])
    assert result.exit_code == 0
    assert (tmp_path / "data_readiness.md").exists()

    content = (tmp_path / "data_readiness.md").read_text(encoding="utf-8")
    assert "不足" in content or "WARN" in content


def test_doctor_creates_readiness_md(cli_runner, tmp_path):
    """lake-skill doctor outputs data_readiness.md with proper structure."""
    runner, app = cli_runner

    from lake_skill.schema import Message, SenderRole, MessageType, Modality
    from datetime import datetime, timedelta
    from lake_skill.jsonl_utils import write_jsonl_models

    messages = []
    for i in range(50):
        role = SenderRole.SELF if i % 2 == 0 else SenderRole.TARGET
        messages.append(Message(
            message_id=f"msg-{i}",
            conversation_id="test-conv",
            source_type="csv",
            timestamp=datetime(2026, 1, 1) + timedelta(days=i // 10),
            sender_role=role,
            message_type=MessageType.TEXT,
            modality=Modality.TEXT,
            text=f"Message {i}",
        ))

    messages_path = tmp_path / "messages.jsonl"
    write_jsonl_models(messages_path, messages)

    result = runner.invoke(app, [
        "doctor",
        "--messages", str(messages_path),
        "--out", str(tmp_path),
    ])
    assert result.exit_code == 0

    content = (tmp_path / "data_readiness.md").read_text(encoding="utf-8")
    assert "LakeSkill Data Readiness Report" in content
    assert "消息量" in content
    assert "时间跨度" in content
    assert "双方平衡" in content


def test_doctor_warns_when_high_volume_lacks_t1(cli_runner, tmp_path):
    """High message volume without T1 relationship signals is not enough for strong relationship claims."""
    runner, app = cli_runner

    from lake_skill.schema import Message, SenderRole, MessageType, Modality
    from datetime import datetime, timedelta
    from lake_skill.jsonl_utils import write_jsonl_models

    messages = []
    for i in range(120):
        role = SenderRole.SELF if i % 2 == 0 else SenderRole.TARGET
        messages.append(Message(
            message_id=f"msg-{i}",
            conversation_id="test-conv",
            source_type="csv",
            timestamp=datetime(2026, 1, 1) + timedelta(hours=i),
            sender_role=role,
            message_type=MessageType.TEXT,
            modality=Modality.TEXT,
            text=f"今天第 {i} 条日常闲聊",
        ))

    messages_path = tmp_path / "messages.jsonl"
    write_jsonl_models(messages_path, messages)

    result = runner.invoke(app, [
        "doctor",
        "--messages", str(messages_path),
        "--out", str(tmp_path),
    ])
    assert result.exit_code == 0

    content = (tmp_path / "data_readiness.md").read_text(encoding="utf-8")
    assert "T1 关系信号" in content
    assert "不足以判断关系性质" in content
