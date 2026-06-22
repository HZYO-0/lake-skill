# LakeSkill

> *"I kept asking AI 'does my crush like me or not?' It always gave a confident answer, but the more I read, the more anxious I got. LakeSkill made me realize — it should have started with 'not enough evidence.'"*

**Don't let AI guess whether they love you. Let the chat evidence speak for itself.**

[中文](README.md) | [Install](INSTALL.md) | [Quickstart](docs/quickstart.md) | [Chat Record Preparation](docs/chat_record_preparation.md)

[![CI](https://github.com/HZYO-0/lake-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/HZYO-0/lake-skill/actions/workflows/ci.yml)
[![Security](https://github.com/HZYO-0/lake-skill/actions/workflows/security.yml/badge.svg)](https://github.com/HZYO-0/lake-skill/actions/workflows/security.yml)

Paste a chat log and LakeSkill will:

- Tell you **what the evidence supports** and what it doesn't — no guessing
- Give you an **action card**: what to do this week, what to avoid, what to say
- Tag every claim with an **evidence ID and confidence level**; downgrades when evidence is thin

> ⚠️ LakeSkill does not roleplay your partner, confirm their true feelings, create emotional dependency, or provide manipulation tactics.

## See It In Action

### Scenario 1: Paste a chat

Input:

```text
Use lake-skill to analyze this chat. My goal is to know what to do next.

[2026-06-01 22:13] Me: You seem a bit less responsive lately. Did I do something wrong?
[2026-06-01 22:18] Them: No, I have just been busy these days.
[2026-06-02 09:10] Them: Do you still have that document from yesterday?
```

The first thing you see is not a personality report. It's an action card:

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

### Scenario 2: Follow-up questions

```text
You: What did that message mean?
```

```markdown
The surface meaning is a practical request, but combined with "been busy lately," it may be testing whether you're still available.
Evidence: E-20260602-001
Confidence: low. Alternative explanation: they may genuinely just need the document.
```

### Scenario 3: When evidence is thin

```text
You: Do they like me or not?
```

```markdown
Current data is insufficient to determine relationship nature. The 3 messages you provided contain no confession, rejection, or relationship definition signals.
Suggested input: more daily interactions, conflict scenarios, conversations they initiated.
```

Want to make screenshots for social media or recording tutorials? Generate public-safe synthetic assets:

```bash
lake-skill demo --out examples/social_demo
```

## Install

```bash
npx skills add HZYO-0/lake-skill -y
```

Or ask an AI agent to install it:

```text
Please find LakeSkill on GitHub and install it into my local agent runtime.
Repository: https://github.com/HZYO-0/lake-skill.git
```

Exporting from WeChat? Use [WeChatDataAnalysis](https://github.com/LifeArchiveProject/WeChatDataAnalysis) (GitHub 1.4k stars) to decrypt WeChat databases, export, then import into LakeSkill.

More install options (Codex, Claude Code, manual, ChatGPT GPT): [INSTALL.md](INSTALL.md).

## How To Use

### Paste directly

After installing the Skill, paste chat records to the agent:

```text
Use lake-skill, analyze my chat records. Give me the action card first.
```

### Tell the agent the file location

If chat records are already exported as files (CSV, TXT, SQLite), tell the agent the file path:

```text
Use lake-skill, analyze the chat records in this file: D:\chats\chat.csv. Give me the action card first.
```

### Preprocess locally then upload

For privacy-sensitive data, redact first:

```bash
lake-skill redact --file chat.jsonl --out chat.redacted.jsonl --privacy-mode cloud-safe
```

Then tell the agent to read the redacted file.

Not sure? Install, paste one chat, try it once. 5 minutes to know.

## Features

### Data Sources

| Source | Format | Notes |
|---|---|---|
| WeChat | WeChatDataAnalysis export (TXT/JSON/SQLite) | Recommended, richest data |
| Generic chat | CSV / TXT / JSONL | Most export tools default format |
| Voice transcripts | SRT / VTT | Timestamped speech recognition |
| OCR text | JSONL / CSV | Text extracted from screenshots |
| Direct paste | Plain text | Fastest way to test |

### Analysis Capabilities

| Capability | Description |
|---|---|
| Action card | First screen answers "what do I do now" with evidence backing |
| Evidence report | 9-layer structure: card → situation → timeline → portraits → patterns → attachment → advice → uncertainty |
| Coaching mode | Follow-up questions with multiple tone drafts |
| Data readiness | doctor 3-tier: local observation / action card / full report |
| Incremental update | New chat records auto-merge into existing analysis |
| Conversation correction | Say "they wouldn't say that" — instant update |

### Privacy

- Local redaction: `lake-skill redact` strips names, phones, addresses
- Leak check: `lake-skill check-leaks` scans for residual private info
- Bundle upload: `lake-skill bundle` only packages redacted artifacts
- Public demo: `lake-skill demo` generates synthetic data, no real chats

## What It Covers

Ambiguous flirting, relationship repair, cold-streak review, boundary communication, message drafts, incremental updates — all using the same evidence framework.

Does not do: medical diagnosis, manipulation tactics, relationship outcome prediction, database decryption.

## Why Trust It

1. **Evidence first, conclusions second**: every claim must have an evidence ID; without it, it's a guess.
2. **Downgrade when uncertain**: when evidence is thin, it gives low-risk observations instead of forcing a full judgment.
3. **Every conclusion has counterevidence**: not just one answer, but what conditions might prove it wrong.

If evidence is insufficient, LakeSkill will explicitly say "current data is insufficient" rather than hiding behind vague wording.

## Why "Lake Mirror"

A lake works like a mirror. Relationship evidence gets reflected first, not amplified by emotion.

In Chinese poetry, lakes carry stories of approach, waiting, missing, and reuniting.

Before looking outward for answers, find your own steadiness first.

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
