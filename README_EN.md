# LakeSkill

> A calm relationship mirror for chat evidence.  
> Not a partner simulator, not a certainty machine.

[中文](README.md) | [Install](INSTALL.md) | [Quickstart](docs/quickstart.md) | [Chat Record Preparation](docs/chat_record_preparation.md) | [Migration](docs/migration_from_bondlens.md)

[![CI](https://github.com/HZYO-0/lake-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/HZYO-0/lake-skill/actions/workflows/ci.yml)
[![Security](https://github.com/HZYO-0/lake-skill/actions/workflows/security.yml/badge.svg)](https://github.com/HZYO-0/lake-skill/actions/workflows/security.yml)

LakeSkill is an evidence-based relationship chat analysis Skill for agent runtimes such as Codex, Claude Code, and OpenCode, with an optional privacy-first local preprocessing CLI. It does not roleplay your partner, ex, coworker, or any specific person. It places chat records on a calmer surface: evidence, timing, signals, boundaries, confidence, and what to do next.

Current versions:

| Component | Version | Notes |
|---|---:|---|
| Skill framework | 0.10.0 | `skills/lake-skill/SKILL.md` |
| Python CLI package | 0.10.0 | Local preprocessing tool named `lake-skill` |
| Install path | `skills/lake-skill/` | Canonical GitHub Skill package |

## Why LakeSkill

A lake can work like a mirror when the surface is still. Relationship interpretation often fails when the surface is not still: anxiety turns one short reply into a conclusion, ambiguity becomes certainty, and a single moment erases the timeline around it.

LakeSkill is designed to slow that down. It separates stronger relationship signals from background noise, keeps claims tied to evidence IDs, marks uncertainty, and gives a low-pressure action card before any long report.

## 30-Second Demo

```text
Use lake-skill to analyze this chat. My goal is to know what to do next.

[2026-06-01 22:13] Me: You seem a bit less responsive lately. Did I do something wrong?
[2026-06-01 22:18] Them: No, I have just been busy these days.
[2026-06-02 09:10] Them: Do you still have that document from yesterday?
```

LakeSkill starts with an action card:

```markdown
## Start Here: Lake Mirror Action Card

### Current Strategy
Low-pressure stability.

Why:
They did not expand on the emotional check-in, but they also did not cut off ordinary interaction.
They initiated a practical request the next morning.
Evidence: E-20260601-001, E-20260602-001
Confidence: low to medium. The sample is too short for a stable relationship-level conclusion.

### 3 Actions This Week
1. Return to a normal rhythm; do not repeatedly ask whether you did something wrong.
2. Respond normally when they ask for help, and do not turn the help into emotional bargaining.
3. If you need to express your feeling, use one low-pressure sentence without asking for an immediate decision.

### Do Not
- Do not open with "why are you not responding to me?"
- Do not read one short reply as proof that they do not care.
- Do not use the analysis result to lecture them.

### Ready-To-Send Message
"I think I was a bit sensitive earlier. I did not mean to pressure you. I will send the document first, and we can talk when you are less busy."
```

## What You Get

- **Lake Mirror action card**: current situation, strategy, this week's actions, what to avoid, signals to watch, and message drafts.
- **Evidence report**: relationship timeline, signal ledger, communication portraits, interaction loops, repair signals, confidence, counterevidence, and alternative explanations.
- **Coaching mode**: follow-up help for "what should I say?", "did I overstep?", or "should I hold steady or escalate?"

LakeSkill does not provide clinical diagnosis, manipulation tactics, deterministic claims about another person's intent, relationship outcome prediction, revival-style simulation, database decryption, or access-control bypass.

## Why Trust It

| Mechanism | Purpose |
|---|---|
| Signal ledger first | Extract relationship signals before writing conclusions |
| T1-T4 weighting | Relationship definitions, refusals, boundaries, and user corrections outrank daily statistics |
| Timeline first | Prevent early refusals from erasing later changes, or later ambiguity from erasing earlier boundaries |
| Multi-factor interpretation | Avoid collapsing conclusions into "likes me / does not like me" or "avoidant / not avoidant" |
| Reliability audit | Check T1 coverage, T4 overreach, single-factor claims, counterevidence, and alternatives |
| Privacy-first CLI | Redact, segment, summarize, and index sensitive data locally before upload |

## Install

```bash
npx skills add HZYO-0/lake-skill -y
```

The installable Skill lives at:

```text
skills/lake-skill/
```

For local preprocessing:

```bash
git clone https://github.com/HZYO-0/lake-skill.git
cd lake-skill
pip install -e ".[dev]"
lake-skill init ./my_project
```

Typical local pipeline:

```bash
lake-skill ingest --file input/chat.csv --type csv --self-name Me --target-name Them --out work/raw_messages.jsonl
lake-skill redact --file work/raw_messages.jsonl --out work/messages.redacted.jsonl --privacy-mode cloud-safe
lake-skill segment --file work/messages.redacted.jsonl --out work/sessions.redacted.jsonl
lake-skill digest --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --out work/digest.redacted.md
lake-skill evidence --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --out work/evidence.redacted.jsonl
```

See [INSTALL.md](INSTALL.md), [docs/quickstart.md](docs/quickstart.md), and [docs/platform_compatibility.md](docs/platform_compatibility.md) for platform-specific setup.

## Project Structure

```text
skills/lake-skill/        Installable Skill package
cli/lake_skill/           Optional local preprocessing CLI
docs/                     User and platform docs
examples/                 Synthetic examples
tests/                    CLI, parser, safety, and audit tests
```

## License

MIT License. See [LICENSE](LICENSE).
