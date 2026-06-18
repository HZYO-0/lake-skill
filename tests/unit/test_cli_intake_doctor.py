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


def test_doctor_report_translates_overall_into_actionability_tier(cli_runner, tmp_path):
    """doctor reports whether the dataset supports local observation, an action card, or a full report."""
    runner, app = cli_runner

    from datetime import datetime, timedelta
    from lake_skill.jsonl_utils import write_jsonl_models
    from lake_skill.schema import Message, MessageType, Modality, SenderRole

    messages = []
    t1_texts = {
        5: "我想认真聊聊我们是什么关系",
        25: "我不是拒绝你，只是想慢慢来",
        45: "以后再看，不想现在就定义关系",
    }
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
            text=t1_texts.get(i, f"今天第 {i} 条日常聊天"),
            text_redacted=t1_texts.get(i, f"今天第 {i} 条日常聊天"),
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
    assert "可出行动卡" in content or "可出完整报告" in content
    assert "只能局部观察" not in content


def test_demo_creates_social_demo_package(cli_runner, tmp_path):
    """lake-skill demo creates synthetic files for README and short-video recording."""
    runner, app = cli_runner
    out_dir = tmp_path / "social_demo"

    result = runner.invoke(app, ["demo", "--out", str(out_dir)])

    assert result.exit_code == 0, result.output
    assert (out_dir / "synthetic_chat.csv").exists()
    assert (out_dir / "work" / "messages.redacted.jsonl").exists()
    assert (out_dir / "work" / "sessions.redacted.jsonl").exists()
    assert (out_dir / "work" / "digest.redacted.md").exists()
    assert (out_dir / "work" / "evidence.redacted.jsonl").exists()
    assert (out_dir / "social_action_card_demo.md").exists()
    social_assets = out_dir / "social_assets"
    assert (social_assets / "xiaohongshu_carousel.md").exists()
    assert (social_assets / "xiaohongshu_caption.md").exists()
    assert (social_assets / "douyin_recording_script.md").exists()
    assert (social_assets / "recording_checklist.md").exists()
    demo_text = (out_dir / "social_action_card_demo.md").read_text(encoding="utf-8")
    assert "湖镜行动卡" in demo_text
    assert "合成示例" in demo_text

    carousel = (social_assets / "xiaohongshu_carousel.md").read_text(encoding="utf-8")
    assert carousel.count("## Page ") >= 6
    assert "合成示例" in carousel

    script = (social_assets / "douyin_recording_script.md").read_text(encoding="utf-8")
    for time_range in ["0-3s", "3-8s", "8-15s", "15-25s", "25-35s"]:
        assert time_range in script
    assert "合成示例" in script

    checklist = (social_assets / "recording_checklist.md").read_text(encoding="utf-8")
    for phrase in [
        "生成 demo",
        "synthetic CSV",
        "行动卡",
        "证据 ID",
        "doctor 三档",
        "bundle 结果",
        "check-leaks",
    ]:
        assert phrase in checklist


def test_bundle_collects_upload_artifacts(cli_runner, tmp_path):
    """lake-skill bundle copies upload-ready artifacts and writes upload_readme.md."""
    runner, app = cli_runner
    source = tmp_path / "source"
    source.mkdir()
    (source / "digest.redacted.md").write_text("# digest\n", encoding="utf-8")
    (source / "sessions.redacted.jsonl").write_text('{"session_id":"s1"}\n', encoding="utf-8")
    (source / "evidence.redacted.jsonl").write_text('{"evidence_id":"E-20260101-001"}\n', encoding="utf-8")
    (source / "lakeskill_intake.yaml").write_text("relationship_type: ambiguous\n", encoding="utf-8")
    out_dir = tmp_path / "bundle"

    result = runner.invoke(app, [
        "bundle",
        "--source", str(source),
        "--out", str(out_dir),
    ])

    assert result.exit_code == 0, result.output
    assert (out_dir / "digest.redacted.md").exists()
    assert (out_dir / "sessions.redacted.jsonl").exists()
    assert (out_dir / "evidence.redacted.jsonl").exists()
    assert (out_dir / "lakeskill_intake.yaml").exists()
    upload_readme = (out_dir / "upload_readme.md").read_text(encoding="utf-8")
    assert "上传给 LakeSkill" in upload_readme
    assert "不要上传原始聊天记录" in upload_readme
    assert "确认材料已脱敏" in upload_readme
    assert "截图" in upload_readme
    assert "语音" in upload_readme
    assert "数据库" in upload_readme
    assert "未获授权" in upload_readme
    assert "危机" in upload_readme
    assert "自伤" in upload_readme
    assert "被威胁" in upload_readme
    assert "未成年人" in upload_readme
    assert "现实支持" in upload_readme
    assert "lake-skill demo" in upload_readme


def test_audit_and_report_lint_cli_wrappers(cli_runner, tmp_path):
    """audit and report-lint expose the script checks through lake-skill CLI."""
    runner, app = cli_runner
    analysis_dir = tmp_path / "analysis"
    analysis_dir.mkdir()

    ledger = analysis_dir / "relationship_signal_ledger.jsonl"
    ledger.write_text(
        '{"evidence_id":"E-20260101-001","date":"2026-01-01","speaker":"target",'
        '"tier":"T1","signal_type":"relationship_definition","quote":"慢慢来",'
        '"local_context":"讨论关系","later_followup":"继续日常互动",'
        '"interpretation_candidates":["不急于定义关系"]}\n',
        encoding="utf-8",
    )
    report = analysis_dir / "lakeskill_report_demo.md"
    report.write_text(
        "# LakeSkill 关系分析报告\n\n"
        "**数据范围**: 2026-01-01 至 2026-01-02\n"
        "**总消息量**: 10 条\n"
        "**抽样说明**: 全量分析\n"
        "## Layer -1: 湖镜行动卡（关系行动卡）\n"
        "证据：E-20260101-001\n"
        "## Layer 0\n## Layer 1\n## Layer 2\n## Layer 3\n"
        "## Layer 4\n## Layer 5\n## Layer 6\n## Layer 7\n",
        encoding="utf-8",
    )

    audit_result = runner.invoke(app, [
        "audit",
        "--ledger", str(ledger),
        "--report", str(report),
    ])
    assert audit_result.exit_code == 0, audit_result.output
    assert "Relationship signal reliability checks passed" in audit_result.output

    lint_result = runner.invoke(app, ["report-lint", str(analysis_dir)])
    assert lint_result.exit_code == 0, lint_result.output
    assert "所有报告通过 lint 检查" in lint_result.output
