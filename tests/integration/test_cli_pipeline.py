"""Integration test: full CLI pipeline from CSV to export."""

import json
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SYNTHETIC_CSV = PROJECT_ROOT / "examples" / "synthetic_input" / "chat.csv"


def _check_cli_deps() -> None:
    """Ensure CLI dependencies are installed."""
    try:
        import typer  # noqa: F401
        import pydantic  # noqa: F401
    except ImportError as e:
        pytest.skip(
            f"CLI dependencies not installed: {e}. "
            "Run: pip install -e '.[dev]'"
        )


@pytest.fixture()
def cli_runner():
    """Provide a Typer CliRunner."""
    from typer.testing import CliRunner
    from bondlens.cli import app
    return CliRunner(), app


def test_full_pipeline(cli_runner: tuple, tmp_path: Path) -> None:
    """ingest -> redact -> segment -> digest -> evidence -> export all succeed."""
    _check_cli_deps()
    runner, app = cli_runner
    work = tmp_path / "work"
    work.mkdir()

    # ingest
    r = runner.invoke(app, [
        "ingest", "-f", str(SYNTHETIC_CSV), "-t", "csv",
        "--self-name", "我", "--target-name", "张三",
        "-o", str(work / "raw.jsonl"),
    ])
    assert r.exit_code == 0, f"ingest failed: {r.stderr if hasattr(r, 'stderr') else r.output}"
    assert (work / "raw.jsonl").exists()

    # redact
    r = runner.invoke(app, [
        "redact", "-f", str(work / "raw.jsonl"),
        "-o", str(work / "redacted.jsonl"),
    ])
    assert r.exit_code == 0, f"redact failed: {r.output}"
    assert (work / "redacted.jsonl").exists()

    # segment
    r = runner.invoke(app, [
        "segment", "-f", str(work / "redacted.jsonl"),
        "-o", str(work / "sessions.jsonl"),
    ])
    assert r.exit_code == 0, f"segment failed: {r.output}"
    assert (work / "sessions.jsonl").exists()

    # digest
    r = runner.invoke(app, [
        "digest", "-m", str(work / "redacted.jsonl"),
        "-s", str(work / "sessions.jsonl"),
        "-o", str(work / "digest.md"),
    ])
    assert r.exit_code == 0, f"digest failed: {r.output}"
    assert (work / "digest.md").exists()

    # evidence
    r = runner.invoke(app, [
        "evidence", "-m", str(work / "redacted.jsonl"),
        "-s", str(work / "sessions.jsonl"),
        "-o", str(work / "evidence.jsonl"),
    ])
    assert r.exit_code == 0, f"evidence failed: {r.output}"
    assert (work / "evidence.jsonl").exists()

    # export (conversations mode)
    r = runner.invoke(app, [
        "export", "-m", str(work / "redacted.jsonl"),
        "-s", str(work / "sessions.jsonl"),
        "-o", str(work / "conversations.jsonl"),
        "--mode", "conversations",
    ])
    assert r.exit_code == 0, f"export failed: {r.output}"
    assert (work / "conversations.jsonl").exists()


def test_jsonl_outputs_are_valid(cli_runner: tuple, tmp_path: Path) -> None:
    """All JSONL outputs contain valid JSON lines."""
    _check_cli_deps()
    runner, app = cli_runner
    work = tmp_path / "work"
    work.mkdir()

    steps = [
        (["ingest", "-f", str(SYNTHETIC_CSV), "-t", "csv",
          "--self-name", "我", "--target-name", "张三",
          "-o", str(work / "raw.jsonl")], "ingest"),
        (["redact", "-f", str(work / "raw.jsonl"),
          "-o", str(work / "redacted.jsonl")], "redact"),
        (["segment", "-f", str(work / "redacted.jsonl"),
          "-o", str(work / "sessions.jsonl")], "segment"),
        (["evidence", "-m", str(work / "redacted.jsonl"),
          "-s", str(work / "sessions.jsonl"),
          "-o", str(work / "evidence.jsonl")], "evidence"),
    ]

    for args, name in steps:
        r = runner.invoke(app, args)
        assert r.exit_code == 0, f"{name} failed: {r.output}"

    for fname in ["raw.jsonl", "redacted.jsonl", "sessions.jsonl", "evidence.jsonl"]:
        fpath = work / fname
        assert fpath.exists(), f"{fname} missing"
        lines = fpath.read_text(encoding="utf-8").strip().splitlines()
        assert len(lines) > 0, f"{fname} is empty"
        for i, line in enumerate(lines):
            obj = json.loads(line)
            assert isinstance(obj, dict), f"{fname} line {i} is not a dict"


def test_digest_contains_sections(cli_runner: tuple, tmp_path: Path) -> None:
    """Digest output contains expected sections."""
    _check_cli_deps()
    runner, app = cli_runner
    work = tmp_path / "work"
    work.mkdir()

    for args in [
        ["ingest", "-f", str(SYNTHETIC_CSV), "-t", "csv",
         "--self-name", "我", "--target-name", "张三",
         "-o", str(work / "raw.jsonl")],
        ["redact", "-f", str(work / "raw.jsonl"),
         "-o", str(work / "redacted.jsonl")],
        ["segment", "-f", str(work / "redacted.jsonl"),
         "-o", str(work / "sessions.jsonl")],
    ]:
        r = runner.invoke(app, args)
        assert r.exit_code == 0, r.output

    r = runner.invoke(app, [
        "digest", "-m", str(work / "redacted.jsonl"),
        "-s", str(work / "sessions.jsonl"),
        "-o", str(work / "digest.md"),
    ])
    assert r.exit_code == 0, r.output

    digest = (work / "digest.md").read_text(encoding="utf-8")
    assert "消息" in digest or "message" in digest.lower()
    assert "会话" in digest or "session" in digest.lower()
