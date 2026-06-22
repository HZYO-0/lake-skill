# Install LakeSkill

LakeSkill has two parts:

| Part | Required? | Purpose |
|---|---:|---|
| `skills/lake-skill/` | Yes | The installable Skill used by Codex, Claude Code, OpenCode, and similar runtimes |
| Python CLI | Optional | Local preprocessing, redaction, session segmentation, digest, and evidence indexing |

For most users, install the Skill first. Install the CLI only if you want privacy-first local preprocessing or large-data workflows.

---

## 1. Install The Skill

### AgentSkills CLI

```bash
npx skills add HZYO-0/lake-skill -y
```

To inspect detected skills before installing:

```bash
npx skills add HZYO-0/lake-skill --list
```

### Ask An AI Agent To Install It

If your AI agent can use the web and your local terminal, paste this request:

```text
请帮我在 GitHub 上找到 LakeSkill 湖镜，并安装到本地 agent runtime。
仓库地址：https://github.com/HZYO-0/lake-skill.git
安装后请确认 skills/lake-skill/SKILL.md 可用。
```

### Codex Built-In Installer

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo HZYO-0/lake-skill \
  --path skills/lake-skill
```

Windows:

```powershell
python C:\Users\<you>\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py `
  --repo HZYO-0/lake-skill `
  --path skills/lake-skill
```

Restart Codex after installing.

### Manual Install

Copy `skills/lake-skill/` into your runtime's skill directory:

| Runtime | Destination |
|---|---|
| Codex project | `.codex/skills/lake-skill/` |
| Claude Code project | `.claude/skills/lake-skill/` |
| OpenCode project | `.opencode/skills/lake-skill/` |
| Agents project | `.agents/skills/lake-skill/` |

Example:

```bash
mkdir -p .codex/skills
cp -r skills/lake-skill .codex/skills/lake-skill
```

---

## 2. Verify Skill Activation

Start a new agent session and ask:

```text
使用 lake-skill，帮我分析一下这段聊天记录
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

## Getting WeChat Data

If your chat records are in WeChat, use [WeChatDataAnalysis](https://github.com/LifeArchiveProject/WeChatDataAnalysis) to decrypt and export them:

1. Get the decryption key: [wx_key](https://github.com/ycccccccy/wx_key)
2. Install WeChatDataAnalysis: [Releases](https://github.com/LifeArchiveProject/WeChatDataAnalysis/releases/latest)
3. Decrypt the database and export chat records as TXT
4. Import: `lake-skill ingest --file chat.txt --type txt --self-name 我 --target-name 对方 --out work/raw_messages.jsonl`

Full guide: [docs/wechat_data_analysis_guide.md](docs/wechat_data_analysis_guide.md)

---

## 4. Optional CLI Install

Use the CLI when raw data is large or privacy-sensitive.

```bash
git clone https://github.com/HZYO-0/lake-skill.git
cd lake-skill
pip install -e ".[dev]"
lake-skill version
```

If you use Conda on Windows, activate the environment before every verification:

```powershell
conda activate skills
$env:PYTHONUTF8="1"
$env:PYTHONIOENCODING="utf-8"
pip install -e ".[dev]"
python -m lake_skill.cli version
```

`pip install` without arguments only prints a pip error. Use `pip install -e ".[dev]"` from the repository root so Typer, Rich, Pydantic, pytest, Ruff, and safety tools are installed in the active environment.

Initialize a local project:

```bash
lake-skill init ./my_project
cd my_project
```

Typical local pipeline:

```bash
lake-skill ingest --file input/chat.csv --type csv --self-name 我 --target-name 对方 --out work/raw_messages.jsonl
lake-skill redact --file work/raw_messages.jsonl --out work/messages.redacted.jsonl --privacy-mode cloud-safe
lake-skill segment --file work/messages.redacted.jsonl --out work/sessions.redacted.jsonl
lake-skill digest --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --out work/digest.redacted.md
lake-skill evidence --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --out work/evidence.redacted.jsonl
lake-skill intake --out work --type ambiguous --status unknown --work-mode practical
lake-skill doctor --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --out work
lake-skill export --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --out work/conversations.jsonl --mode conversations
lake-skill bundle --source work --out upload_bundle
```

Upload these processed files to the Skill:

- `work/digest.redacted.md`
- `work/sessions.redacted.jsonl`
- `work/evidence.redacted.jsonl`
- `work/lakeskill_intake.yaml` if generated
- `work/conversations.jsonl` if you want richer analysis

---

## 5. ChatGPT Custom GPT Setup

1. Create a custom GPT.
2. Paste `skills/lake-skill/SKILL.md` into Instructions.
3. Upload files from `skills/lake-skill/references/frameworks/` to Knowledge.
4. Upload prompt modules from `skills/lake-skill/prompts/` if the GPT supports enough Knowledge files.
5. Start with representative chat records or local preprocessing outputs.

ChatGPT setup is less deterministic than a native Skill runtime because it does not execute the same local workflow. Prefer Codex or Claude Code for full reports, evidence indexing, and local preprocessing.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Skill does not activate | Restart the runtime and verify `skills/lake-skill/SKILL.md` is installed under the correct folder |
| Output is too generic | Provide more messages and at least 3 scene types |
| Agent makes strong claims | Ask it to rerun with LakeSkill safety boundaries and cite evidence IDs |
| Privacy concern | Use CLI redaction and upload only redacted digest/evidence/session files |
| SQLite import fails | Confirm the database is plaintext SQLite; LakeSkill does not decrypt protected databases |
| `ModuleNotFoundError: typer` | Activate the intended environment and run `pip install -e ".[dev]"` from the repository root |
| Chinese output crashes on Windows | Set `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8` before running checks |
