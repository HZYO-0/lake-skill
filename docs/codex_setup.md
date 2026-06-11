# Codex Setup

## Install from GitHub

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo HZYO-0/lake-skill \
  --path skills/lake-skill
```

Windows example:

```powershell
python C:\Users\<you>\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py `
  --repo HZYO-0/lake-skill `
  --path skills/lake-skill
```

Restart Codex after installing.

## Install with AgentSkills CLI

```bash
npx skills add HZYO-0/lake-skill -y
```

## Verify

After restarting Codex, ask:

```text
使用 lake-skill，帮我分析一下这段聊天记录
```

LakeSkill should activate only when chat records, redacted CLI exports, or relationship-message drafting requests are present.

## Manual Project Install

```bash
mkdir -p .codex/skills
cp -r skills/lake-skill .codex/skills/lake-skill
```

Project-local installs are useful for testing, but published GitHub installs should use the `skills/lake-skill/` subdirectory.
