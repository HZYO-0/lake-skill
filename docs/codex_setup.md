# Codex Setup

## Install from GitHub

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo HZYO-0/bondlens \
  --path skills/bondlens
```

Windows example:

```powershell
python C:\Users\<you>\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py `
  --repo HZYO-0/bondlens `
  --path skills/bondlens
```

Restart Codex after installing.

## Install with AgentSkills CLI

```bash
npx skills add HZYO-0/bondlens -y
```

## Verify

After restarting Codex, ask:

```text
使用 bondlens，帮我分析一下这段聊天记录
```

BondLens should activate only when chat records, redacted CLI exports, or relationship-message drafting requests are present.

## Manual Project Install

```bash
mkdir -p .codex/skills
cp -r skills/bondlens .codex/skills/bondlens
```

Project-local installs are useful for testing, but published GitHub installs should use the `skills/bondlens/` subdirectory.
