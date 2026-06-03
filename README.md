# BondLens 关系镜

Evidence-based relationship chat analysis for ChatGPT, Claude Code, Codex, OpenCode, OpenClaw, and other Skill/Agent runtimes.

BondLens does **not** tell you "TA is definitely avoidant." It says: "these messages show avoidant-adjacent signals, confidence is medium, counterevidence includes..., and alternative explanations are..."

[![CI](https://github.com/HZYO-0/bondlens/actions/workflows/ci.yml/badge.svg)](https://github.com/HZYO-0/bondlens/actions/workflows/ci.yml)
[![Security](https://github.com/HZYO-0/bondlens/actions/workflows/security.yml/badge.svg)](https://github.com/HZYO-0/bondlens/actions/workflows/security.yml)

## Why BondLens

- **Evidence first**: major claims cite evidence IDs, confidence levels, counterevidence, and alternative explanations.
- **Non-clinical**: personality and attachment outputs are communication hypotheses, not diagnoses.
- **Privacy-aware**: paste directly for convenience, or use the CLI to redact and summarize locally before upload.
- **Coaching mode**: turns analysis into safer message drafts and next-step communication options.
- **Portable Skill**: one canonical installable package in `skills/bondlens/`, packaged for multiple agent runtimes.

## Install

### One-line install

In Claude Code, Codex, OpenCode, or another compatible agent, ask:

```text
帮我安装这个 skill：https://github.com/HZYO-0/bondlens/tree/main/skills/bondlens
```

If your runtime supports AgentSkills:

```bash
npx skills add HZYO-0/bondlens -y
```

For Codex's built-in skill installer:

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo HZYO-0/bondlens \
  --path skills/bondlens
```

### ChatGPT Custom GPT

1. Create a GPT.
2. Paste [`skills/bondlens/SKILL.md`](skills/bondlens/SKILL.md) into **Instructions**.
3. Upload the 7 files in [`skills/bondlens/references/frameworks/`](skills/bondlens/references/frameworks/) to **Knowledge**.
4. Start with a representative chat record sample.

Manual platform paths and verification steps are in [`INSTALL.md`](INSTALL.md).

## Quick Start

After installing, say:

```text
帮我分析一下我们的聊天记录
```

Then paste or upload chat records:

```text
以下是我和某人的聊天记录，请帮我分析：

2025-05-21 22:13 张三: 今天其实有点想你
2025-05-21 22:14 我: 真的吗？我也在想你
2025-05-21 22:15 张三: 嗯嗯，最近工作有点累
2025-05-21 22:16 我: 辛苦了，周末要不要一起吃饭
...
```

For a full portrait, provide enough context:

| Input | Expected behavior |
|---|---|
| 5-10 messages | Low-confidence local observations only |
| 30+ messages across multiple sessions | Initial calibrated analysis |
| 100+ messages across varied scenarios | Stronger relationship portrait and interaction-pattern analysis |
| CLI redacted export | Full analysis with better privacy control |

See [`docs/chat_record_preparation.md`](docs/chat_record_preparation.md) for what to include.

## What It Produces

BondLens produces an 8-layer relationship analysis report:

| Layer | Content |
|-------|---------|
| Layer 0 | Core interaction rules (when TA approaches, withdraws, conflicts, repairs) |
| Layer 1 | Relationship background and key patterns |
| Layer 2 | Target's expression DNA (catchphrases, rhythm, emotional expressions) |
| Layer 3 | Your expression DNA (same structure) |
| Layer 4 | Interaction patterns (positive/negative loops, conflict escalation, repair signals) |
| Layer 5 | Attachment signals (anxiety/avoidance/secure for both parties) |
| Layer 6 | Communication coaching + multi-tone message drafts |
| Layer 7 | Uncertainty notes (confidence, counterevidence, alternative explanations) |

Every major conclusion cites evidence IDs, confidence levels, and alternative explanations.

When data is insufficient, BondLens asks a short calibration question set first. If the user wants to skip, it proceeds with explicitly low-confidence observations.

## Supported Inputs

| Source | Formats | Notes |
|---|---|---|
| WeChat desktop export | TXT, CSV | Best for direct upload or CLI preprocessing |
| Generic tables | CSV, TSV | Requires timestamp, sender, and content columns |
| Structured messages | JSONL | Best for repeatable workflows |
| Plaintext SQLite | `.db`, `.sqlite` | CLI only; no decryption or key extraction |
| Voice transcripts | SRT, VTT, JSONL | Preserves ASR confidence when available |
| OCR transcripts | CSV, JSONL | Analyzes extracted text, not raw screenshots |

BondLens only analyzes user-provided and authorized data. It will not decrypt databases, bypass access controls, scrape private accounts, or help access someone else's records.

## Privacy Modes

| Mode | Raw data leaves your machine? | Best for |
|---|---:|---|
| Direct paste/upload | Yes | Fast trial, small private samples you are comfortable uploading |
| CLI local preprocessing | No | Sensitive data, large histories, repeatable analysis |

The output structure is the same in both modes. Analysis quality depends on data quantity, context diversity, and how much detail remains after redaction.

## CLI Privacy Workflow

Use the CLI when you want local preprocessing before uploading anything to a cloud agent.

```bash
git clone https://github.com/HZYO-0/bondlens.git
cd bondlens
pip install -e ".[dev]"

bondlens init ./my-project
cd my-project

bondlens ingest --file input/chat.csv --type csv --self-name 我 --target-name 对方
bondlens redact --file work/raw_messages.jsonl --out work/messages.redacted.jsonl
bondlens segment --file work/messages.redacted.jsonl --out work/sessions.redacted.jsonl
bondlens digest --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --out work/digest.redacted.md
bondlens evidence --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --out work/evidence.redacted.jsonl
bondlens export --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --out work/conversations.jsonl --mode conversations
bondlens kb init --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --evidence work/evidence.redacted.jsonl --out kb/
bondlens kb patch --kb kb/ --evidence work/evidence.redacted.jsonl --out work/patch.json
```

Upload these generated files to your Skill/Agent:

- `work/digest.redacted.md`
- `work/sessions.redacted.jsonl`
- `work/evidence.redacted.jsonl`
- `work/conversations.jsonl`
- `kb/*.md` if using a relationship knowledge base

## Safety Boundaries

BondLens refuses or redirects requests for:

- clinical diagnosis, personality disorder labeling, or mental health assessment
- manipulation, PUA, coercion, jealousy induction, stalking, or emotional blackmail
- certainty claims about another person's intentions or feelings
- relationship outcome prediction
- decrypting or bypassing protected chat databases

## Repository Layout

```text
.
├── skills/bondlens/              # Installable Skill package for GitHub/AgentSkills
│   ├── SKILL.md                  # Canonical Skill instruction (v2, 5-step workflow)
│   ├── references/frameworks/    # Evidence, attachment, personality, safety, and coaching frameworks
│   ├── assets/kb_template/       # Relationship knowledge-base templates
│   └── agents/openai.yaml        # UI metadata for compatible skill runtimes
├── skill/prompts/                # Structured analysis prompts (intake, analyzers, report, merge, correction)
├── cli/bondlens/                 # Optional Python CLI for local preprocessing
├── docs/                         # Installation, privacy, platform, and data-preparation guides
├── examples/                     # Synthetic inputs and output-structure checks
├── tests/                        # Unit, integration, and safety tests
└── tools/                        # Verification, packaging, and scanners
```

## Verify Locally

```bash
pip install -e ".[dev]"
python tools/check.py --quick
python tools/check.py
python tools/package_skill.py
```

`check.py --quick` runs ruff, tests, privacy scanning, and forbidden-network-call scanning. The full check also runs advisory mypy.

## Documentation

- [`INSTALL.md`](INSTALL.md): install paths for ChatGPT, Claude Code, Codex, OpenCode, OpenClaw, and Agents
- [`docs/chat_record_preparation.md`](docs/chat_record_preparation.md): what chat data to prepare for the first analysis
- [`docs/privacy_model.md`](docs/privacy_model.md): direct mode vs. local preprocessing mode
- [`docs/platform_compatibility.md`](docs/platform_compatibility.md): runtime-specific skill packaging notes
- [`SECURITY.md`](SECURITY.md): security policy and reporting guidance

## Current Limitations

- The CLI is source-installed for now: `pip install -e ".[dev]"`.
- SQLite support is for readable plaintext databases only.
- Audio/image media must be transcribed first; BondLens analyzes text transcripts.

## License

MIT License. See [`LICENSE`](LICENSE).
