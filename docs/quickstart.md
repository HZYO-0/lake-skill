# Quickstart Guide

## Installation

```bash
pip install bondlens
```

## Initialize Project

```bash
bondlens init ./my_project
cd my_project
```

## Prepare Your Data

Place your chat data in the `input/` directory. Supported formats:
- CSV files
- TXT files (WeChat export format)
- SQLite databases
- Voice transcripts (SRT/VTT)
- OCR transcripts

## Ingest Data

### CSV Format

```bash
bondlens ingest --file input/chat.csv --type csv --self-name 我 --target-name 对方 --out work/raw_messages.jsonl
```

### TXT Format (WeChat Export)

```bash
bondlens ingest --file input/chat.txt --type txt --self-name 我 --target-name 对方 --out work/raw_messages.jsonl
```

### SQLite Database

```bash
bondlens ingest --file input/chat.db --type sqlite --self-id wxid_me --target-id wxid_target --out work/raw_messages.jsonl
```

## Redact Sensitive Information

```bash
bondlens redact --file work/raw_messages.jsonl --out work/messages.redacted.jsonl --privacy-mode cloud-safe
```

## Segment Sessions

```bash
bondlens segment --file work/messages.redacted.jsonl --out work/sessions.redacted.jsonl
```

## Generate Digest

```bash
bondlens digest --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --out work/digest.redacted.md
```

## Index Evidence

```bash
bondlens evidence --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --out work/evidence.redacted.jsonl
```

## Initialize Knowledge Base

```bash
bondlens kb init --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --evidence work/evidence.redacted.jsonl --out kb/
```

## Next Steps

1. Upload `work/digest.redacted.md`, `work/sessions.redacted.jsonl`, and `work/evidence.redacted.jsonl` to ChatGPT Skill
2. Review the generated reports
3. Update your knowledge base with new data
