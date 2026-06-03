# Platform Compatibility

BondLens uses one canonical installable package:

```text
skills/bondlens/
```

That folder contains `SKILL.md`, framework references, knowledge-base templates, and optional agent metadata. The repository root is for development and CLI tooling.

## Recommended Install

Use AgentSkills-compatible installation when available:

```bash
npx skills add HZYO-0/bondlens -y
```

To preview what the repository exposes:

```bash
npx skills add HZYO-0/bondlens --list
```

## Codex

Codex can install the GitHub subdirectory directly:

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo HZYO-0/bondlens \
  --path skills/bondlens
```

Restart Codex after installation.

## ChatGPT Custom GPT

1. Create a GPT.
2. Paste `skills/bondlens/SKILL.md` into **Instructions**.
3. Upload all files from `skills/bondlens/references/frameworks/` to **Knowledge**.
4. Paste or upload representative chat records.

## Claude Project

Use the same ChatGPT-style paste/upload model:

1. Paste `skills/bondlens/SKILL.md` into the project instructions.
2. Upload `skills/bondlens/references/frameworks/*.md` as project knowledge.

## Manual Copy Paths

Copy `skills/bondlens/` into the target runtime path:

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
mkdir -p .claude/skills
cp -r skills/bondlens .claude/skills/bondlens
```

## Package Layout

```text
skills/bondlens/
├── SKILL.md
├── agents/openai.yaml
├── references/frameworks/
│   ├── evidence_ladder.md
│   ├── big_five_communication_signals.md
│   ├── attachment_anxiety_avoidance.md
│   ├── relationship_communication_patterns.md
│   ├── forbidden_overclaims.md
│   ├── symbolic_mode_policy.md
│   └── coaching_dialogue_framework.md
└── assets/kb_template/
```

## Packaging

Generate platform-specific archives with:

```bash
python tools/package_skill.py
```

The generated `dist/` directory is disposable and not committed.
