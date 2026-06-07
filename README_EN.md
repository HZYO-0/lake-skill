# BondLens

> Not a partner simulator. An evidence-based relationship action card.

[中文](README.md) | [Install](INSTALL.md) | [Quickstart](docs/quickstart.md) | [Chat Record Preparation](docs/chat_record_preparation.md)

[![CI](https://github.com/HZYO-0/bondlens/actions/workflows/ci.yml/badge.svg)](https://github.com/HZYO-0/bondlens/actions/workflows/ci.yml)
[![Security](https://github.com/HZYO-0/bondlens/actions/workflows/security.yml/badge.svg)](https://github.com/HZYO-0/bondlens/actions/workflows/security.yml)

BondLens is an evidence-based relationship chat analysis Skill for agent runtimes such as Codex, Claude Code, and OpenCode, with an optional local preprocessing CLI. It does not simulate your partner, ex, coworker, or any specific person. It turns chat records into an auditable relationship action card: what is happening, what to do this week, what not to overclaim, and what to say next.

Current versions:

| Component | Version | Notes |
|---|---:|---|
| Skill framework | 0.9.0 | `skills/bondlens/SKILL.md` |
| Python CLI package | 0.9.0 | Local preprocessing tool named `bondlens` |
| Install path | `skills/bondlens/` | Canonical GitHub Skill package |

---

## 30-Second Demo

Input can be short:

```text
Use bondlens to analyze this chat. My goal is to know what to do next.

[2026-06-01 22:13] Me: You seem a bit less responsive lately. Did I do something wrong?
[2026-06-01 22:18] Them: No, I have just been busy these days.
[2026-06-02 09:10] Them: Do you still have that document from yesterday?
```

BondLens starts with an action card, not a long personality essay:

```markdown
## Start Here: Relationship Action Card

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

---

## How BondLens Differs From ex-skill / colleague-skill

Many Skill-community projects focus on person distillation or persona simulation: packaging an ex, coworker, role, or memory into something an agent can speak through. BondLens takes a different path. It does not roleplay the other person; it interprets evidence.

| Type | Typical Goal | Typical Output | BondLens Difference |
|---|---|---|---|
| dot-skill / colleague-style | Distill a person, coworker, or role into a Skill | Feedback, banter, review, or advice in that persona | BondLens does not imitate a voice; it analyzes what the chat evidence supports |
| ex-skill-style | Turn a past relationship into an interactive persona | Memory-like interaction, emotional replay, simulated dialogue | BondLens does not revive a relationship object or predict someone's true inner state |
| BondLens | Turn chat logs into action judgment | Action cards, evidence reports, message drafts, audit notes | The core is evidence interpretation + action coaching |

One-line positioning: Stop asking AI to guess whether they love you. Let BondLens show what the chat evidence supports, what it does not support, and what to do next without overstepping.

---

## What You Get

### Relationship Action Card

The first screen answers "what should I do now?"

- Current situation and recent trend
- Current strategy: low-pressure stability / careful escalation / conflict repair
- 3 concrete actions for this week
- Things not to do
- Previous risk points
- Signals to watch next
- Ready-to-send message drafts

### Evidence Report

The full report explains why the action card says what it says:

- Relationship timeline and key events
- Relationship signal ledger summary
- Communication portraits anchored in quotes
- Interaction loops, conflict paths, and repair signals
- Non-clinical attachment-signal hypotheses
- Confidence, counterevidence, and alternative explanations for major claims

### Coaching Mode

You can keep asking:

```text
What should I say?
What does this sentence mean?
Did I step on a boundary?
Should I escalate or hold steady?
Does this message feel too pressuring?
```

BondLens gives concrete wording based on evidence, confidence, and boundaries. It does not provide manipulation strategies.

---

## Why Trust It

BondLens is designed to make relationship interpretation auditable instead of more confident-sounding.

| Mechanism | Purpose |
|---|---|
| Signal ledger first | Extract relationship signals before writing conclusions |
| T1-T4 weighting | Relationship definitions, refusals, boundaries, and user corrections outrank daily statistics |
| Timeline first | Prevent early refusals from erasing later changes, or later ambiguity from erasing earlier boundaries |
| Multi-factor interpretation | Avoid collapsing conclusions into "likes me / does not like me" or "avoidant / not avoidant" |
| Reliability audit | Check T1 coverage, T4 overreach, single-factor claims, counterevidence, and alternative explanations |
| Confidence and counterevidence | Major claims should include confidence, counterevidence, and other possible explanations |
| Privacy-first CLI | Large or sensitive data can be redacted, segmented, summarized, and indexed locally before upload |

If the data is too thin, BondLens should downgrade the output: local, low-confidence observations only, without full personality or relationship-level conclusions.

---

## Use Cases

| Scenario | What BondLens Can Do |
|---|---|
| Ambiguous romantic escalation | Decide whether to lightly escalate, hold steady, or pause, with low-pressure wording |
| Relationship repair | Review the conflict path, repair signals, and the next sentence that reduces defensiveness |
| Cold-reply analysis | Separate short-term busyness, pressure avoidance, boundary signals, and interaction cooling |
| Boundary communication | Express needs without interrogation, pressure, or weaponizing the analysis |
| Message drafting | Generate warm, direct, pressure-reducing, or boundary-aware versions |
| Incremental updates | Merge new chat records and user corrections into an evolving knowledge base |

BondLens does not provide:

- Clinical diagnosis
- PUA, manipulation, jealousy induction, or cold-treatment testing
- Deterministic claims about another person's intention
- Relationship outcome prediction
- Revival-style simulation of an ex, partner, or coworker
- Database decryption or access-control bypass

---

## Install

Install the Skill:

```bash
npx skills add HZYO-0/bondlens -y
```

Preview detected Skills:

```bash
npx skills add HZYO-0/bondlens --list
```

The installable Skill lives at:

```text
skills/bondlens/
```

See [INSTALL.md](INSTALL.md) and [docs/platform_compatibility.md](docs/platform_compatibility.md) for Codex, Claude Code, OpenCode, manual install, and ChatGPT Custom GPT setup.

---

## Quickstart

After installation, start a new agent session:

```text
Use bondlens to analyze our chat records.
```

Then provide one of these inputs:

- Pasted chat excerpts
- TXT/CSV/JSONL chat files
- Local preprocessing outputs: `digest`, `sessions`, `evidence`, and optional knowledge-base files

For large or privacy-sensitive data, preprocess locally:

```bash
git clone https://github.com/HZYO-0/bondlens.git
cd bondlens
pip install -e ".[dev]"
bondlens init ./my_project
```

Typical local pipeline:

```bash
bondlens ingest --file input/chat.csv --type csv --self-name Me --target-name Them --out work/raw_messages.jsonl
bondlens redact --file work/raw_messages.jsonl --out work/messages.redacted.jsonl --privacy-mode cloud-safe
bondlens segment --file work/messages.redacted.jsonl --out work/sessions.redacted.jsonl
bondlens digest --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --out work/digest.redacted.md
bondlens evidence --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --out work/evidence.redacted.jsonl
```

See [docs/quickstart.md](docs/quickstart.md) and [docs/chat_record_preparation.md](docs/chat_record_preparation.md) for more detail.

---

## How Much Chat Data Is Enough

Short excerpts can still be useful, but stable relationship-level interpretation needs enough context.

| Data Amount | Suitable For | Expected Confidence |
|---|---|---|
| 5-30 messages | Local scene reading and one reply draft | Low |
| 30-100 messages | Initial communication-signal check | Low to medium |
| 100+ messages across several days | Action card + focused report | Medium |
| Weeks or months with varied scenes | Full report + playbook + knowledge base | Medium to high |

Recommended scenes:

- Daily chat
- Help-seeking or practical support
- Conflict or pressure
- Repair or apology
- Cold or delayed replies
- Warm or intimate moments
- Boundary discussions

---

## Workflow

1. **Intake**: relationship type, current status, names, analysis goal, data source.
2. **Data check**: message count, time span, participation balance, scene variety.
3. **Local preprocessing**: optional redaction, session segmentation, digest, evidence indexing.
4. **Signal ledger**: extract T1-T4 relationship signals and contradictions first.
5. **Action card**: answer what to do next before the long report.
6. **Full report**: Layer -1 through Layer 7 evidence report.
7. **Audit**: evidence completeness, risky language, coverage statement, uncertainty checks.
8. **Update**: merge new data and user corrections into the knowledge base.

---

## Report Structure

| Layer | Purpose |
|---|---|
| Layer -1 | Relationship action card |
| Layer 0 | Core behavior rules |
| Layer 0.5 | Current situation |
| Layer 1 | Relationship background and timeline |
| Layer 1.5 | Relationship signal ledger summary |
| Layer 2 | Their portrait with quote anchoring |
| Layer 3 | Your portrait with quote anchoring |
| Layer 4 | Interaction patterns |
| Layer 5 | Non-clinical attachment signals |
| Layer 6 | Communication playbook and message drafts |
| Layer 7 | Uncertainty, counterevidence, alternative explanations |

---

## Project Structure

```text
skills/bondlens/           Installable Skill package
  SKILL.md                 Skill instructions
  prompts/                 Analysis and coaching prompt modules
  references/frameworks/   Evidence, attachment, communication, safety frameworks
  assets/kb_template/      Incremental knowledge-base templates
cli/bondlens/              Optional local preprocessing CLI
docs/                      User, platform compatibility, and promotion docs
examples/                  Synthetic example inputs and expected output structures
tests/                     CLI, parser, safety, and audit tests
```

---

## License

MIT License. See [LICENSE](LICENSE).
