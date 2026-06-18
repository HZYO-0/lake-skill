# Privacy Model

## Overview

LakeSkill supports two usage modes with different privacy characteristics:

**Direct Mode** — Paste or upload chat records directly to the Skill. Data passes through the platform (ChatGPT, Claude, etc.). Quick to start, lower privacy.

**Local Preprocessing Mode** — Use the CLI to process data on your machine. Only redacted digests, session summaries, and evidence indices leave your machine. Maximum privacy.

Both modes produce the same output structure. Actual analysis quality depends on data volume, redaction level, and context completeness.

## Privacy Modes

### local-raw

- **Use case**: Complete local processing, no sharing
- **Behavior**: No redaction, strong warnings
- **Warning**: Do not upload outputs to cloud, GitHub, or public chat windows

### local-safe

- **Use case**: Local reports, low-risk sharing
- **Behavior**: Redacts high-risk identifiers
- **Redacts**: Phone numbers, ID cards, addresses, WeChat IDs, emails, bank cards

### cloud-safe (Default)

- **Use case**: Uploading to ChatGPT Skill
- **Behavior**: Redacts names, organizations, locations, contact info, financial data
- **Redacts**: Names, WeChat IDs, phone numbers, emails, companies/schools, addresses, amounts, coordinates, ID cards, bank cards
- **Preserves**: Emotional semantics, relationship semantics, coarse time, interaction order, evidence IDs

### publish-safe

- **Use case**: Public examples, issues, test fixtures
- **Behavior**: Only allows synthetic data
- **Requirement**: Must use synthetic data only

## What Gets Uploaded

Default upload files:
- `work/digest.redacted.md`
- `work/sessions.redacted.jsonl`
- `work/evidence.redacted.jsonl`
- `kb/metadata.yaml`
- `kb/*.md` (if existing knowledge base)

## What Stays Local

- Original `.db` files
- Original `.csv/.txt/.html` files
- Original voice recordings
- Original screenshots
- Complete unredacted chat text

## Security Features

1. **Deterministic hashing**: Messages are hashed for consistent identification
2. **Leak checker**: Scans outputs for sensitive information
3. **Privacy mode validation**: Ensures correct mode for use case
4. **No telemetry**: No network uploads by default
