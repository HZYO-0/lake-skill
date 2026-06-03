"""WeChat Relationship Insight CLI."""

from pathlib import Path
from typing import Optional

import typer
from rich import print as rprint

from .config import BondLensConfig, save_config

app = typer.Typer(
    name="bondlens",
    help="Privacy-first local preprocessing toolkit for intimate relationship chat analysis.",
    no_args_is_help=True,
)

VERSION = "0.1.0"


@app.command()
def init(
    path: str = typer.Argument(".", help="Path to initialize project"),
) -> None:
    """Initialize a new BondLens project."""
    project_path = Path(path)
    rprint(f"[green]Initializing BondLens project at {project_path}[/green]")

    # Create directory structure
    dirs = [
        "input",
        "work",
        "kb",
        "reports",
        "examples",
    ]

    for dir_name in dirs:
        dir_path = project_path / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        rprint(f"  Created {dir_path}/")

    # Create default config
    config = BondLensConfig()
    config_path = project_path / "config.yaml"
    save_config(config, config_path)
    rprint(f"  Created {config_path}")

    # Create .gitignore if not exists
    gitignore_path = project_path / ".gitignore"
    if not gitignore_path.exists():
        gitignore_content = """# BondLens project data
input/
work/
kb/
reports/
*.db
*.sqlite
*.sqlite3
*.csv
*.jsonl
*.json
*.txt
*.html
*.htm
*.srt
*.vtt

# Python
__pycache__/
*.py[cod]
.venv/
.env
.pytest_cache/
.mypy_cache/
.ruff_cache/
dist/
build/
*.egg-info/
"""
        gitignore_path.write_text(gitignore_content, encoding="utf-8")
        rprint(f"  Created {gitignore_path}")

    rprint("[green]Project initialized successfully![/green]")
    rprint("\nNext steps:")
    rprint("  1. Place your chat data in the input/ directory")
    rprint("  2. Run 'bondlens ingest' to process your data")


@app.command()
def version() -> None:
    """Show version."""
    rprint(f"[blue]bondlens v{VERSION}[/blue]")


@app.command()
def ingest(
    file: str = typer.Option(..., "--file", "-f", help="Input file path"),
    type: str = typer.Option("auto", "--type", "-t", help="Input type (csv, txt, jsonl, sqlite, voice-transcript, ocr-transcript, auto)"),
    out: str = typer.Option("work/raw_messages.jsonl", "--out", "-o", help="Output file path"),
    self_name: Optional[str] = typer.Option(None, "--self-name", help="Name of self user"),
    target_name: Optional[str] = typer.Option(None, "--target-name", help="Name of target user"),
    self_id: Optional[str] = typer.Option(None, "--self-id", help="ID of self user (for SQLite)"),
    target_id: Optional[str] = typer.Option(None, "--target-id", help="ID of target user (for SQLite)"),
    conversation: Optional[str] = typer.Option(None, "--conversation", help="Conversation ID to filter"),
    schema_map: Optional[str] = typer.Option(None, "--schema-map", help="Schema map file for SQLite"),
    sender_role: str = typer.Option("target", "--sender-role", help="Sender role for voice/OCR transcripts"),
) -> None:
    """Ingest chat data from various formats."""
    from .adapters.base import BaseAdapter
    from .adapters.generic_csv import GenericCSVAdapter
    from .adapters.generic_jsonl import GenericJSONLAdapter
    from .adapters.wechat_txt import WeChatTXTAdapter
    from .adapters.wechat_sqlite import WeChatSQLiteAdapter
    from .adapters.voice_transcript import VoiceTranscriptAdapter
    from .adapters.ocr_transcript import OCRTranscriptAdapter
    from .schema import SenderRole as SenderRoleEnum

    file_path = Path(file)
    output_path = Path(out)
    warnings_path = output_path.parent / "parse_warnings.jsonl"

    if not file_path.exists():
        rprint(f"[red]Error: File not found: {file_path}[/red]")
        raise typer.Exit(1)

    # Auto-detect type if not specified
    if type == "auto":
        suffix = file_path.suffix.lower()
        if suffix == ".csv":
            type = "csv"
        elif suffix in (".txt", ".text"):
            type = "txt"
        elif suffix in (".jsonl", ".json"):
            type = "jsonl"
        elif suffix in (".db", ".sqlite", ".sqlite3"):
            type = "sqlite"
        elif suffix in (".srt", ".vtt"):
            type = "voice-transcript"
        else:
            rprint(f"[red]Error: Cannot auto-detect type for {suffix}[/red]")
            raise typer.Exit(1)

    # Parse sender role
    try:
        role = SenderRoleEnum(sender_role)
    except ValueError:
        rprint(f"[red]Error: Invalid sender role: {sender_role}[/red]")
        raise typer.Exit(1)

    # Load schema map if provided
    schema_map_data = None
    if schema_map:
        import yaml
        with open(schema_map, "r", encoding="utf-8") as f:
            schema_map_data = yaml.safe_load(f)

    # Select adapter
    adapter: BaseAdapter
    if type == "csv":
        adapter = GenericCSVAdapter(
            warnings_path=warnings_path,
            self_name=self_name,
            target_name=target_name,
        )
    elif type == "txt":
        adapter = WeChatTXTAdapter(
            warnings_path=warnings_path,
            self_name=self_name,
            target_name=target_name,
        )
    elif type == "jsonl":
        adapter = GenericJSONLAdapter(warnings_path=warnings_path)
    elif type == "sqlite":
        adapter = WeChatSQLiteAdapter(
            warnings_path=warnings_path,
            schema_map=schema_map_data,
            self_id=self_id,
            target_id=target_id,
            conversation_id=conversation,
        )
    elif type == "voice-transcript":
        adapter = VoiceTranscriptAdapter(
            warnings_path=warnings_path,
            sender_role=role,
            conversation_id=conversation,
        )
    elif type == "ocr-transcript":
        adapter = OCRTranscriptAdapter(
            warnings_path=warnings_path,
            sender_role=role,
            conversation_id=conversation,
        )
    else:
        rprint(f"[red]Error: Unsupported type: {type}[/red]")
        raise typer.Exit(1)

    # Process file
    rprint(f"[blue]Processing {file_path} as {type}...[/blue]")
    count = adapter.process(file_path, output_path)
    rprint(f"[green]Processed {count} messages -> {output_path}[/green]")

    if adapter.warnings:
        rprint(f"[yellow]Warning: {len(adapter.warnings)} warnings -> {warnings_path}[/yellow]")


@app.command()
def redact(
    file: str = typer.Option(..., "--file", "-f", help="Input file path"),
    out: str = typer.Option(..., "--out", "-o", help="Output file path"),
    privacy_mode: str = typer.Option("cloud-safe", "--privacy-mode", "-p", help="Privacy mode"),
) -> None:
    """Redact sensitive information from messages."""
    from .privacy.modes import validate_privacy_mode
    from .privacy.redactor import create_redactor
    from .jsonl_utils import read_jsonl, write_jsonl

    file_path = Path(file)
    output_path = Path(out)

    if not file_path.exists():
        rprint(f"[red]Error: File not found: {file_path}[/red]")
        raise typer.Exit(1)

    # Validate privacy mode
    try:
        mode = validate_privacy_mode(privacy_mode)
    except ValueError as e:
        rprint(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)

    # Check for publish-safe mode
    if mode.value == "publish-safe":
        rprint("[red]Error: publish-safe mode requires synthetic data only[/red]")
        raise typer.Exit(1)

    # Create redactor
    redactor = create_redactor(mode)

    # Process file
    rprint(f"[blue]Redacting {file_path} with {privacy_mode} mode...[/blue]")

    messages = list(read_jsonl(file_path))
    redacted_messages = [redactor.redact_message(msg) for msg in messages]
    write_jsonl(output_path, redacted_messages)

    rprint(f"[green]Redacted {len(redacted_messages)} messages -> {output_path}[/green]")

    # Show warning for local-raw mode
    if mode.value == "local-raw":
        rprint("[yellow]Warning: local-raw mode does not redact. Do not upload to cloud.[/yellow]")


@app.command()
def check_leaks(
    dir: str = typer.Argument(".", help="Directory to check"),
) -> None:
    """Check for privacy leaks in directory."""
    from .privacy.leak_checker import check_for_leaks

    dir_path = Path(dir)

    if not dir_path.exists():
        rprint(f"[red]Error: Directory not found: {dir_path}[/red]")
        raise typer.Exit(1)

    rprint(f"[blue]Checking {dir_path} for privacy leaks...[/blue]")

    has_leaks, report = check_for_leaks(dir_path)

    if has_leaks:
        rprint(f"[red]{report}[/red]")
        raise typer.Exit(1)
    else:
        rprint("[green]No privacy leaks detected.[/green]")


@app.command()
def segment(
    file: str = typer.Option(..., "--file", "-f", help="Input file path"),
    out: str = typer.Option(..., "--out", "-o", help="Output file path"),
    time_gap: float = typer.Option(6.0, "--time-gap", help="Time gap threshold (hours)"),
) -> None:
    """Segment messages into sessions."""
    from .jsonl_utils import read_jsonl, write_jsonl_models
    from .schema import Message
    from .segmentation.sessionizer import segment_sessions

    file_path = Path(file)
    output_path = Path(out)

    if not file_path.exists():
        rprint(f"[red]Error: File not found: {file_path}[/red]")
        raise typer.Exit(1)

    # Read messages
    rprint(f"[blue]Reading messages from {file_path}...[/blue]")
    messages = [Message(**data) for data in read_jsonl(file_path)]
    rprint(f"  Loaded {len(messages)} messages")

    # Segment sessions
    rprint(f"[blue]Segmenting sessions (time gap: {time_gap}h)...[/blue]")
    sessions = segment_sessions(messages, time_gap_hours=time_gap)
    rprint(f"  Created {len(sessions)} sessions")

    # Save sessions
    write_jsonl_models(output_path, sessions)
    rprint(f"[green]Saved sessions -> {output_path}[/green]")


@app.command()
def digest(
    messages_file: str = typer.Option(..., "--messages", "-m", help="Messages file path"),
    sessions_file: str = typer.Option(..., "--sessions", "-s", help="Sessions file path"),
    out: str = typer.Option(..., "--out", "-o", help="Output file path"),
) -> None:
    """Generate relationship digest."""
    from .jsonl_utils import read_jsonl
    from .schema import Message, Session
    from .reports.digest import generate_digest

    messages_path = Path(messages_file)
    sessions_path = Path(sessions_file)
    output_path = Path(out)

    if not messages_path.exists():
        rprint(f"[red]Error: Messages file not found: {messages_path}[/red]")
        raise typer.Exit(1)
    if not sessions_path.exists():
        rprint(f"[red]Error: Sessions file not found: {sessions_path}[/red]")
        raise typer.Exit(1)

    # Read data
    rprint(f"[blue]Reading messages from {messages_path}...[/blue]")
    messages = [Message(**data) for data in read_jsonl(messages_path)]
    rprint(f"  Loaded {len(messages)} messages")

    rprint(f"[blue]Reading sessions from {sessions_path}...[/blue]")
    sessions = [Session(**data) for data in read_jsonl(sessions_path)]
    rprint(f"  Loaded {len(sessions)} sessions")

    # Generate digest
    rprint("[blue]Generating digest...[/blue]")
    generate_digest(messages, sessions, str(output_path))
    rprint(f"[green]Generated digest -> {output_path}[/green]")


@app.command()
def evidence(
    messages_file: str = typer.Option(..., "--messages", "-m", help="Messages file path"),
    sessions_file: str = typer.Option(..., "--sessions", "-s", help="Sessions file path"),
    out: str = typer.Option(..., "--out", "-o", help="Output file path"),
) -> None:
    """Generate evidence index."""
    from .jsonl_utils import read_jsonl
    from .schema import Message, Session
    from .evidence.indexer import index_evidence, save_evidence_index

    messages_path = Path(messages_file)
    sessions_path = Path(sessions_file)
    output_path = Path(out)

    if not messages_path.exists():
        rprint(f"[red]Error: Messages file not found: {messages_path}[/red]")
        raise typer.Exit(1)
    if not sessions_path.exists():
        rprint(f"[red]Error: Sessions file not found: {sessions_path}[/red]")
        raise typer.Exit(1)

    # Read data
    rprint(f"[blue]Reading messages from {messages_path}...[/blue]")
    messages = [Message(**data) for data in read_jsonl(messages_path)]
    rprint(f"  Loaded {len(messages)} messages")

    rprint(f"[blue]Reading sessions from {sessions_path}...[/blue]")
    sessions = [Session(**data) for data in read_jsonl(sessions_path)]
    rprint(f"  Loaded {len(sessions)} sessions")

    # Index evidence
    rprint("[blue]Indexing evidence...[/blue]")
    evidence_list = index_evidence(messages, sessions)
    rprint(f"  Created {len(evidence_list)} evidence items")

    # Save evidence index
    save_evidence_index(evidence_list, str(output_path))
    rprint(f"[green]Saved evidence index -> {output_path}[/green]")


# KB subcommand group
kb_app = typer.Typer(help="Knowledge base management commands.")
app.add_typer(kb_app, name="kb")


@kb_app.command("init")
def kb_init(
    messages_file: str = typer.Option(..., "--messages", "-m", help="Messages file path"),
    sessions_file: str = typer.Option(..., "--sessions", "-s", help="Sessions file path"),
    evidence_file: str = typer.Option(..., "--evidence", "-e", help="Evidence file path"),
    out: str = typer.Option(..., "--out", "-o", help="Output directory path"),
) -> None:
    """Initialize knowledge base."""
    from .jsonl_utils import read_jsonl
    from .schema import Message, Session, Evidence
    from .kb.init import initialize_kb

    messages_path = Path(messages_file)
    sessions_path = Path(sessions_file)
    evidence_path = Path(evidence_file)
    output_path = Path(out)

    # Check files exist
    for path, name in [(messages_path, "Messages"), (sessions_path, "Sessions"), (evidence_path, "Evidence")]:
        if not path.exists():
            rprint(f"[red]Error: {name} file not found: {path}[/red]")
            raise typer.Exit(1)

    # Read data
    rprint(f"[blue]Reading messages from {messages_path}...[/blue]")
    messages = [Message(**data) for data in read_jsonl(messages_path)]
    rprint(f"  Loaded {len(messages)} messages")

    rprint(f"[blue]Reading sessions from {sessions_path}...[/blue]")
    sessions = [Session(**data) for data in read_jsonl(sessions_path)]
    rprint(f"  Loaded {len(sessions)} sessions")

    rprint(f"[blue]Reading evidence from {evidence_path}...[/blue]")
    evidence_list = [Evidence(**data) for data in read_jsonl(evidence_path)]
    rprint(f"  Loaded {len(evidence_list)} evidence items")

    # Initialize KB
    rprint("[blue]Initializing knowledge base...[/blue]")
    kb = initialize_kb(messages, sessions, evidence_list, str(output_path))
    rprint(f"[green]Initialized knowledge base -> {output_path}[/green]")
    rprint(f"  Observations: {len(kb.observations)}")


@kb_app.command("patch")
def kb_patch(
    kb_dir: str = typer.Option(..., "--kb", help="Knowledge base directory"),
    evidence_file: str = typer.Option(..., "--evidence", "-e", help="New evidence file path"),
    out: str = typer.Option(..., "--out", "-o", help="Output patch file path"),
) -> None:
    """Create knowledge base patch."""
    from .jsonl_utils import read_jsonl
    from .schema import Evidence
    from .kb.patch import create_kb_patch, save_kb_patch

    kb_path = Path(kb_dir)
    evidence_path = Path(evidence_file)
    output_path = Path(out)

    # Check files exist
    if not kb_path.exists():
        rprint(f"[red]Error: KB directory not found: {kb_path}[/red]")
        raise typer.Exit(1)
    if not evidence_path.exists():
        rprint(f"[red]Error: Evidence file not found: {evidence_path}[/red]")
        raise typer.Exit(1)

    # Load existing KB from directory
    from .kb.init import load_kb
    kb = load_kb(str(kb_path))

    # Read new evidence
    rprint(f"[blue]Reading new evidence from {evidence_path}...[/blue]")
    new_evidence = [Evidence(**data) for data in read_jsonl(evidence_path)]
    rprint(f"  Loaded {len(new_evidence)} evidence items")

    # Create patch
    rprint("[blue]Creating KB patch...[/blue]")
    patch = create_kb_patch(kb, new_evidence)

    # Save patch
    save_kb_patch(patch, str(output_path))
    rprint(f"[green]Saved KB patch -> {output_path}[/green]")
    rprint(f"  Summary: {patch.summary}")


@app.command()
def export(
    messages_file: str = typer.Option(..., "--messages", "-m", help="Redacted messages file path"),
    sessions_file: str = typer.Option(..., "--sessions", "-s", help="Sessions file path"),
    out: str = typer.Option(..., "--out", "-o", help="Output file path"),
    mode: str = typer.Option("conversations", "--mode", help="Export mode: summary, conversations, full"),
) -> None:
    """Export data for AI analysis.

    Modes:
      summary       - Only digest + evidence + session stats (max privacy, least context)
      conversations - Full message sequences with redaction (balanced)
      full          - Everything including raw messages (max analysis, local only)
    """
    from .jsonl_utils import read_jsonl
    from .schema import Message, Session

    messages_path = Path(messages_file)
    sessions_path = Path(sessions_file)
    output_path = Path(out)

    if not messages_path.exists():
        rprint(f"[red]Error: Messages file not found: {messages_path}[/red]")
        raise typer.Exit(1)
    if not sessions_path.exists():
        rprint(f"[red]Error: Sessions file not found: {sessions_path}[/red]")
        raise typer.Exit(1)

    if mode not in ("summary", "conversations", "full"):
        rprint(f"[red]Error: Invalid mode: {mode}. Use summary, conversations, or full.[/red]")
        raise typer.Exit(1)

    # Read data
    rprint(f"[blue]Reading messages from {messages_path}...[/blue]")
    messages = [Message(**data) for data in read_jsonl(messages_path)]
    rprint(f"  Loaded {len(messages)} messages")

    rprint(f"[blue]Reading sessions from {sessions_path}...[/blue]")
    sessions = [Session(**data) for data in read_jsonl(sessions_path)]
    rprint(f"  Loaded {len(sessions)} sessions")

    # Build message lookup
    msg_lookup = {m.message_id: m for m in messages}

    import json

    if mode == "summary":
        # Only session stats - current behavior
        rprint("[blue]Exporting summary mode (stats only)...[/blue]")
        with open(output_path, "w", encoding="utf-8") as f:
            for session in sessions:
                entry = {
                    "session_id": session.session_id,
                    "start": session.start.isoformat(),
                    "end": session.end.isoformat(),
                    "message_count": session.message_count,
                    "self_count": session.self_count,
                    "target_count": session.target_count,
                    "topic": session.topic,
                    "episode_type": session.episode_type,
                    "risk_level": session.risk_level,
                }
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        rprint(f"[green]Exported {len(sessions)} session summaries -> {output_path}[/green]")

    elif mode == "conversations":
        # Full message sequences within sessions (redacted text)
        rprint("[blue]Exporting conversations mode (full sequences, redacted text)...[/blue]")
        with open(output_path, "w", encoding="utf-8") as f:
            for session in sessions:
                session_messages = []
                for msg_id in session.message_ids:
                    msg = msg_lookup.get(msg_id)
                    if msg:
                        # Use redacted text if available, otherwise original
                        text = msg.text_redacted or msg.text or ""
                        session_messages.append({
                            "message_id": msg.message_id,
                            "speaker": msg.sender_role.value,
                            "text": text,
                            "timestamp": msg.timestamp.isoformat(),
                            "message_type": msg.message_type.value,
                        })

                entry = {
                    "session_id": session.session_id,
                    "start": session.start.isoformat(),
                    "end": session.end.isoformat(),
                    "message_count": len(session_messages),
                    "self_count": session.self_count,
                    "target_count": session.target_count,
                    "topic": session.topic,
                    "episode_type": session.episode_type,
                    "risk_level": session.risk_level,
                    "messages": session_messages,
                }
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        rprint(f"[green]Exported {len(sessions)} conversations -> {output_path}[/green]")
        rprint("[yellow]Note: This file contains full conversation text (redacted). Review before uploading.[/yellow]")

    elif mode == "full":
        # Everything including raw messages
        rprint("[blue]Exporting full mode (all data)...[/blue]")
        with open(output_path, "w", encoding="utf-8") as f:
            for session in sessions:
                session_messages = []
                for msg_id in session.message_ids:
                    msg = msg_lookup.get(msg_id)
                    if msg:
                        session_messages.append({
                            "message_id": msg.message_id,
                            "speaker": msg.sender_role.value,
                            "text": msg.text or "",
                            "text_redacted": msg.text_redacted or "",
                            "raw_text": msg.raw_text or "",
                            "timestamp": msg.timestamp.isoformat(),
                            "message_type": msg.message_type.value,
                            "modality": msg.modality.value,
                            "quality": {  # type: ignore[dict-item]
                                "parse_confidence": msg.quality.parse_confidence.value if msg.quality.parse_confidence else None,
                                "asr_confidence": str(msg.quality.asr_confidence) if msg.quality.asr_confidence is not None else None,
                                "ocr_confidence": str(msg.quality.ocr_confidence) if msg.quality.ocr_confidence is not None else None,
                            },
                        })

                entry = {
                    "session_id": session.session_id,
                    "start": session.start.isoformat(),
                    "end": session.end.isoformat(),
                    "message_count": len(session_messages),
                    "self_count": session.self_count,
                    "target_count": session.target_count,
                    "topic": session.topic,
                    "episode_type": session.episode_type,
                    "risk_level": session.risk_level,
                    "dominant_emotion": session.dominant_emotion,
                    "messages": session_messages,
                }
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        rprint(f"[green]Exported {len(sessions)} conversations (full) -> {output_path}[/green]")
        rprint("[red]Warning: This file contains raw text. Do NOT upload to cloud services.[/red]")


if __name__ == "__main__":
    app()
