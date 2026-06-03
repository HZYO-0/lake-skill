# Installation

BondLens has one clean installable Skill package:

```text
skills/bondlens/
```

The repository root is the development project. Use `skills/bondlens/` when installing the Skill.

## AgentSkills CLI

For Claude Code, Codex, OpenCode, OpenClaw, and other compatible runtimes:

```bash
npx skills add HZYO-0/bondlens -y
```

To list detected skills first:

```bash
npx skills add HZYO-0/bondlens --list
```

## Codex Built-In Installer

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo HZYO-0/bondlens \
  --path skills/bondlens
```

On Windows, the script path is usually:

```powershell
python C:\Users\<you>\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py `
  --repo HZYO-0/bondlens `
  --path skills/bondlens
```

Restart Codex after installing.

## ChatGPT Custom GPT

1. Create a GPT.
2. Paste `skills/bondlens/SKILL.md` into **Instructions**.
3. Upload all 7 files from `skills/bondlens/references/frameworks/` to **Knowledge**.
4. Start with representative chat records.

## Manual Install Paths

Copy the contents of `skills/bondlens/` into the relevant runtime path:

| Platform | Destination |
|---|---|
| Claude Code project | `.claude/skills/bondlens/` |
| Claude Code global | `~/.claude/skills/bondlens/` |
| Codex project | `.codex/skills/bondlens/` |
| OpenCode project | `.opencode/skills/bondlens/` |
| OpenClaw global | `~/.openclaw/workspace/skills/bondlens/` |
| Agents project | `.agents/skills/bondlens/` |

Example:

```bash
mkdir -p .codex/skills
cp -r skills/bondlens .codex/skills/bondlens
```

## Verify

After installation, start a new agent session and say:

```text
帮我分析一下我们的聊天记录
```

If BondLens asks for relationship context, analysis goals, data format, time span, or background, the Skill is active.

## CLI Dependencies

The Python CLI is optional and only needed for local preprocessing:

```bash
pip install -e ".[dev]"
```
