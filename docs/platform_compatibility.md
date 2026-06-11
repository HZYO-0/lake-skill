# Platform Compatibility

LakeSkill uses one canonical installable package:

```text
skills/lake-skill/
```

That folder contains `SKILL.md`, framework references, knowledge-base templates, and optional agent metadata. The repository root is for development and CLI tooling.

## Recommended Install

Use AgentSkills-compatible installation when available:

```bash
npx skills add HZYO-0/lake-skill -y
```

To preview what the repository exposes:

```bash
npx skills add HZYO-0/lake-skill --list
```

## Codex

Codex can install the GitHub subdirectory directly:

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo HZYO-0/lake-skill \
  --path skills/lake-skill
```

Restart Codex after installation.

## ChatGPT Custom GPT

1. Create a GPT.
2. Paste `skills/lake-skill/SKILL.md` into **Instructions**.
3. Upload all files from `skills/lake-skill/references/frameworks/` to **Knowledge**.
4. Paste or upload representative chat records.

## Claude Project

Use the same ChatGPT-style paste/upload model:

1. Paste `skills/lake-skill/SKILL.md` into the project instructions.
2. Upload `skills/lake-skill/references/frameworks/*.md` as project knowledge.

## Manual Copy Paths

Copy `skills/lake-skill/` into the target runtime path:

| Platform | Destination |
|---|---|
| Claude Code project | `.claude/skills/lake-skill/` |
| Claude Code global | `~/.claude/skills/lake-skill/` |
| Codex project | `.codex/skills/lake-skill/` |
| OpenCode project | `.opencode/skills/lake-skill/` |
| OpenClaw global | `~/.openclaw/workspace/skills/lake-skill/` |
| Agents project | `.agents/skills/lake-skill/` |

Example:

```bash
mkdir -p .claude/skills
cp -r skills/lake-skill .claude/skills/lake-skill
```

## Package Layout

```text
skills/lake-skill/
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
