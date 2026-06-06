# Install BondLens

BondLens has two parts:

| Part | Required? | Purpose |
|---|---:|---|
| `skills/bondlens/` | Yes | The installable Skill used by Codex, Claude Code, OpenCode, and similar runtimes |
| Python CLI | Optional | Local preprocessing, redaction, session segmentation, digest, and evidence indexing |

For most users, install the Skill first. Install the CLI only if you want privacy-first local preprocessing or large-data workflows.

---

## 1. Install The Skill

### AgentSkills CLI

```bash
npx skills add HZYO-0/bondlens -y
```

To inspect detected skills before installing:

```bash
npx skills add HZYO-0/bondlens --list
```

### Codex Built-In Installer

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo HZYO-0/bondlens \
  --path skills/bondlens
```

Windows:

```powershell
python C:\Users\<you>\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py `
  --repo HZYO-0/bondlens `
  --path skills/bondlens
```

Restart Codex after installing.

### Manual Install

Copy `skills/bondlens/` into your runtime's skill directory:

| Runtime | Destination |
|---|---|
| Codex project | `.codex/skills/bondlens/` |
| Claude Code project | `.claude/skills/bondlens/` |
| OpenCode project | `.opencode/skills/bondlens/` |
| Agents project | `.agents/skills/bondlens/` |

Example:

```bash
mkdir -p .codex/skills
cp -r skills/bondlens .codex/skills/bondlens
```

---

## 2. Verify Skill Activation

Start a new agent session and ask:

```text
使用 bondlens，帮我分析一下这段聊天记录
```

The Skill is active if the agent asks for relationship context, data source, time span, or analysis goal, or if it produces a relationship action card before the detailed report.

---

## 3. Prepare Enough Chat Records

For a first meaningful analysis, provide more than one isolated exchange.

| Input | Expected output |
|---|---|
| 5-30 messages | Local observation and a reply draft |
| 30-100 messages | Initial pattern check |
| 100+ messages across several days | Action card and focused report |
| Weeks or months with varied scenes | Full report, playbook, and knowledge-base update |

Recommended scenes: daily chat, help-seeking, cold replies, conflict, repair, warm moments, boundary discussions.

See [docs/chat_record_preparation.md](docs/chat_record_preparation.md).

---

## 4. Optional CLI Install

Use the CLI when raw data is large or privacy-sensitive.

```bash
git clone https://github.com/HZYO-0/bondlens.git
cd bondlens
pip install -e ".[dev]"
bondlens version
```

Initialize a local project:

```bash
bondlens init ./my_project
cd my_project
```

Typical local pipeline:

```bash
bondlens ingest --file input/chat.csv --type csv --self-name 我 --target-name 对方 --out work/raw_messages.jsonl
bondlens redact --file work/raw_messages.jsonl --out work/messages.redacted.jsonl --privacy-mode cloud-safe
bondlens segment --file work/messages.redacted.jsonl --out work/sessions.redacted.jsonl
bondlens digest --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --out work/digest.redacted.md
bondlens evidence --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --out work/evidence.redacted.jsonl
bondlens export --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --out work/conversations.jsonl --mode conversations
```

Upload these processed files to the Skill:

- `work/digest.redacted.md`
- `work/sessions.redacted.jsonl`
- `work/evidence.redacted.jsonl`
- `work/conversations.jsonl` if you want richer analysis

---

## 5. ChatGPT Custom GPT Setup

1. Create a custom GPT.
2. Paste `skills/bondlens/SKILL.md` into Instructions.
3. Upload files from `skills/bondlens/references/frameworks/` to Knowledge.
4. Upload prompt modules from `skills/bondlens/prompts/` if the GPT supports enough Knowledge files.
5. Start with representative chat records or local preprocessing outputs.

ChatGPT setup is less deterministic than a native Skill runtime because it does not execute the same local workflow. Prefer Codex or Claude Code for full reports, evidence indexing, and local preprocessing.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Skill does not activate | Restart the runtime and verify `skills/bondlens/SKILL.md` is installed under the correct folder |
| Output is too generic | Provide more messages and at least 3 scene types |
| Agent makes strong claims | Ask it to rerun with BondLens safety boundaries and cite evidence IDs |
| Privacy concern | Use CLI redaction and upload only redacted digest/evidence/session files |
| SQLite import fails | Confirm the database is plaintext SQLite; BondLens does not decrypt protected databases |
