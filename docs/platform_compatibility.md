# Platform Compatibility

WRI's `skill/SKILL.md` is a platform-neutral instruction file. Below are the specific installation paths for each supported platform.

## ChatGPT Custom GPT

1. Open ChatGPT → Create a GPT
2. Paste `skill/SKILL.md` into **Instructions**
3. Upload the 7 framework files from `skill/references/frameworks/` to **Knowledge**
4. Start by pasting chat records directly

No manifest or metadata file needed — ChatGPT uses the Instructions/Knowledge split.

## Claude Code / Claude Projects

**Option A: Claude Project**

1. Create a Project
2. Paste `skill/SKILL.md` into **Instructions**
3. Upload framework files to **Knowledge**

**Option B: Claude Code Skills (local)**

Copy files into `.claude/skills/bondlens/`:

```bash
mkdir -p .claude/skills/bondlens/references/frameworks
cp skill/SKILL.md .claude/skills/bondlens/
cp skill/references/frameworks/*.md .claude/skills/bondlens/references/frameworks/
```

Claude Code discovers skills in `.claude/skills/` automatically. The `SKILL.md` file serves as the primary instruction; framework files are loaded as supporting context.

## OpenCode

OpenCode discovers skills from multiple paths:

- `.opencode/skills/<skill-name>/`
- `.claude/skills/<skill-name>/`
- `.agents/skills/<skill-name>/`

Copy to any of these:

```bash
mkdir -p .opencode/skills/bondlens/references/frameworks
cp skill/SKILL.md .opencode/skills/bondlens/
cp skill/references/frameworks/*.md .opencode/skills/bondlens/references/frameworks/
```

## Codex

Copy to `.codex/skills/bondlens/`:

```bash
mkdir -p .codex/skills/bondlens/references/frameworks
cp skill/SKILL.md .codex/skills/bondlens/
cp skill/references/frameworks/*.md .codex/skills/bondlens/references/frameworks/
```

Or use the agent install prompt from [`INSTALL.md`](../INSTALL.md).

## OpenClaw

Copy to `~/.openclaw/workspace/skills/bondlens/` (global):

```bash
mkdir -p ~/.openclaw/workspace/skills/bondlens/references/frameworks
cp skill/SKILL.md ~/.openclaw/workspace/skills/bondlens/
cp skill/references/frameworks/*.md ~/.openclaw/workspace/skills/bondlens/references/frameworks/
```

## Agents (Generic)

Copy to `.agents/skills/bondlens/`:

```bash
mkdir -p .agents/skills/bondlens/references/frameworks
cp skill/SKILL.md .agents/skills/bondlens/
cp skill/references/frameworks/*.md .agents/skills/bondlens/references/frameworks/
```

## Installation Models

| Model | Description | Platforms |
|-------|-------------|-----------|
| **Project-local** | Skill files in project directory | Claude Code, Codex, OpenCode, Agents |
| **Global** | Skill files in user home directory | Claude Code (`~/.claude/`), OpenClaw (`~/.openclaw/`) |
| **Paste + Upload** | Paste SKILL.md to Instructions, upload frameworks to Knowledge | ChatGPT, Claude Projects |

Project-local takes precedence over global when both exist.

## Canonical Source

All platforms use the same `skill/SKILL.md`. There is no platform-specific variant. If a platform requires additional metadata, create it alongside (not instead of) the canonical file.

## File Structure

```
skill/
├── SKILL.md                              # Primary instruction (canonical)
├── references/frameworks/
│   ├── evidence_ladder.md
│   ├── big_five_communication_signals.md
│   ├── attachment_anxiety_avoidance.md
│   ├── relationship_communication_patterns.md
│   ├── forbidden_overclaims.md
│   ├── symbolic_mode_policy.md
│   └── coaching_dialogue_framework.md
└── assets/kb_template/                   # KB templates (12 files)
```
