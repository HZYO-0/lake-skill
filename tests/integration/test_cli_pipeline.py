"""Integration test: full CLI pipeline from CSV to export."""

import json
import os
import subprocess
import sys
import tempfile
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


def _run(cmd: list[str], work_dir: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = f"{PROJECT_ROOT}{os.pathsep}{existing}" if existing else str(PROJECT_ROOT)
    return subprocess.run(
        cmd, cwd=str(PROJECT_ROOT), capture_output=True, text=True, timeout=30, env=env
    )


def test_full_pipeline() -> None:
    """ingest → redact → segment → digest → evidence → export all succeed."""
    _check_cli_deps()
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / "work"
        work.mkdir()

        # ingest
        r = _run(
            [sys.executable, "-m", "bondlens.cli",
             "ingest", "-f", str(SYNTHETIC_CSV), "-t", "csv",
             "--self-name", "我", "--target-name", "张三",
             "-o", str(work / "raw.jsonl")],
            work,
        )
        assert r.returncode == 0, f"ingest failed: {r.stderr}"
        assert (work / "raw.jsonl").exists()

        # redact
        r = _run(
            [sys.executable, "-m", "bondlens.cli",
             "redact", "-f", str(work / "raw.jsonl"),
             "-o", str(work / "redacted.jsonl")],
            work,
        )
        assert r.returncode == 0, f"redact failed: {r.stderr}"
        assert (work / "redacted.jsonl").exists()

        # segment
        r = _run(
            [sys.executable, "-m", "bondlens.cli",
             "segment", "-f", str(work / "redacted.jsonl"),
             "-o", str(work / "sessions.jsonl")],
            work,
        )
        assert r.returncode == 0, f"segment failed: {r.stderr}"
        assert (work / "sessions.jsonl").exists()

        # digest
        r = _run(
            [sys.executable, "-m", "bondlens.cli",
             "digest", "-m", str(work / "redacted.jsonl"),
             "-s", str(work / "sessions.jsonl"),
             "-o", str(work / "digest.md")],
            work,
        )
        assert r.returncode == 0, f"digest failed: {r.stderr}"
        assert (work / "digest.md").exists()

        # evidence
        r = _run(
            [sys.executable, "-m", "bondlens.cli",
             "evidence", "-m", str(work / "redacted.jsonl"),
             "-s", str(work / "sessions.jsonl"),
             "-o", str(work / "evidence.jsonl")],
            work,
        )
        assert r.returncode == 0, f"evidence failed: {r.stderr}"
        assert (work / "evidence.jsonl").exists()

        # export (conversations mode)
        r = _run(
            [sys.executable, "-m", "bondlens.cli",
             "export", "-m", str(work / "redacted.jsonl"),
             "-s", str(work / "sessions.jsonl"),
             "-o", str(work / "conversations.jsonl"),
             "--mode", "conversations"],
            work,
        )
        assert r.returncode == 0, f"export failed: {r.stderr}"
        assert (work / "conversations.jsonl").exists()


def test_jsonl_outputs_are_valid() -> None:
    """All JSONL outputs contain valid JSON lines."""
    _check_cli_deps()
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / "work"
        work.mkdir()

        steps = [
            ([sys.executable, "-m", "bondlens.cli",
              "ingest", "-f", str(SYNTHETIC_CSV), "-t", "csv",
              "--self-name", "我", "--target-name", "张三",
              "-o", str(work / "raw.jsonl")], "ingest"),
            ([sys.executable, "-m", "bondlens.cli",
              "redact", "-f", str(work / "raw.jsonl"),
              "-o", str(work / "redacted.jsonl")], "redact"),
            ([sys.executable, "-m", "bondlens.cli",
              "segment", "-f", str(work / "redacted.jsonl"),
              "-o", str(work / "sessions.jsonl")], "segment"),
            ([sys.executable, "-m", "bondlens.cli",
              "evidence", "-m", str(work / "redacted.jsonl"),
              "-s", str(work / "sessions.jsonl"),
              "-o", str(work / "evidence.jsonl")], "evidence"),
        ]

        for cmd, name in steps:
            r = _run(cmd, work)
            assert r.returncode == 0, f"{name} failed: {r.stderr}"

        for fname in ["raw.jsonl", "redacted.jsonl", "sessions.jsonl", "evidence.jsonl"]:
            fpath = work / fname
            assert fpath.exists(), f"{fname} missing"
            lines = fpath.read_text(encoding="utf-8").strip().splitlines()
            assert len(lines) > 0, f"{fname} is empty"
            for i, line in enumerate(lines):
                obj = json.loads(line)
                assert isinstance(obj, dict), f"{fname} line {i} is not a dict"


def test_digest_contains_sections() -> None:
    """Digest output contains expected sections."""
    _check_cli_deps()
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / "work"
        work.mkdir()

        for cmd in [
            [sys.executable, "-m", "bondlens.cli",
             "ingest", "-f", str(SYNTHETIC_CSV), "-t", "csv",
             "--self-name", "我", "--target-name", "张三",
             "-o", str(work / "raw.jsonl")],
            [sys.executable, "-m", "bondlens.cli",
             "redact", "-f", str(work / "raw.jsonl"),
             "-o", str(work / "redacted.jsonl")],
            [sys.executable, "-m", "bondlens.cli",
             "segment", "-f", str(work / "redacted.jsonl"),
             "-o", str(work / "sessions.jsonl")],
        ]:
            r = _run(cmd, work)
            assert r.returncode == 0, r.stderr

        r = _run(
            [sys.executable, "-m", "bondlens.cli",
             "digest", "-m", str(work / "redacted.jsonl"),
             "-s", str(work / "sessions.jsonl"),
             "-o", str(work / "digest.md")],
            work,
        )
        assert r.returncode == 0, r.stderr

        digest = (work / "digest.md").read_text(encoding="utf-8")
        assert "消息" in digest or "message" in digest.lower()
        assert "会话" in digest or "session" in digest.lower()
