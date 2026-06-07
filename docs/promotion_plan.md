# BondLens Promotion Plan

## Positioning

BondLens should be presented as a relationship evidence analyzer for the Skill community, not as a partner, ex, or coworker simulator.

Core positioning:

```text
Not a partner simulator. An evidence-based relationship action card.
```

Chinese positioning:

```text
不是把 TA 复活，而是帮你根据聊天证据少踩雷。
```

Short Chinese launch line:

```text
别再让 AI 猜 TA 爱不爱你。让 BondLens 告诉你：聊天证据支持什么、不支持什么、下一步怎么做更安全。
```

Short English launch line:

```text
BondLens turns relationship chat logs into evidence-backed action cards: what is happening, what not to overclaim, and what to say next.
```

## GitHub Setup

Recommended GitHub About description:

```text
Evidence-based relationship chat analysis Skill with action cards, signal ledgers, reliability audits, and privacy-first local preprocessing.
```

Recommended repository topics:

```text
ai-skill
agent-skills
relationship-analysis
wechat
privacy-first
evidence-based
codex
claude-code
openai
chat-analysis
```

Suggested README badges:

- CI workflow
- Security workflow
- Optional release or package workflow once releases are stable

## Skill Directory Listing

Title:

```text
BondLens - Evidence-Based Relationship Chat Analysis
```

Short description:

```text
Turn chat records into relationship action cards with signal ledgers, confidence levels, counterevidence, and privacy-first preprocessing.
```

Long description:

```text
BondLens is an agent Skill for analyzing intimate relationship chat records without pretending to be the other person. It reads pasted chats or locally preprocessed exports, builds a relationship signal ledger, checks evidence sufficiency, and produces an action card before the full report. Outputs include what to do this week, what not to overclaim, ready-to-send messages, confidence levels, counterevidence, alternative explanations, and safety boundaries. For sensitive or large datasets, the optional CLI can redact, segment, summarize, and index evidence locally before upload.
```

Key differentiators:

- Action card first, long report second
- Evidence ledger before conclusions
- T1-T4 signal weighting and timeline-first interpretation
- Reliability audit for overclaims and missing counterevidence
- Privacy-first local preprocessing CLI
- Explicit refusal of diagnosis, manipulation, and persona simulation

## Launch Posts

Chinese post:

```text
我做了一个新的 agent skill：BondLens 关系镜。

它不是前任模拟器，也不是让 AI 猜 TA 爱不爱你。

它做一件更实用的事：把聊天记录变成一张可执行的关系行动卡。

- 现在是什么局势
- 本周怎么做
- 哪些判断不能过度解读
- 哪些雷别踩
- 下一句话怎么发

核心机制是 evidence first：先建关系信号台账，再做判断；每个主要结论尽量给证据、置信度、反证和替代解释。数据敏感时，也可以先用本地 CLI 脱敏、切分、摘要和建证据索引。

安装：
npx skills add HZYO-0/bondlens -y
```

English post:

```text
I built BondLens, an agent Skill for evidence-based relationship chat analysis.

It is not a partner simulator, an ex simulator, or a persona replay tool.

It turns relationship chat logs into an action card:

- what is happening now
- what to do this week
- what not to overclaim
- what not to say
- what message to send next

The workflow is evidence first: build a relationship signal ledger, weight key signals, check uncertainty, and then generate the action card and full report. For sensitive datasets, the optional CLI can redact, segment, summarize, and index evidence locally before upload.

Install:
npx skills add HZYO-0/bondlens -y
```

## Comparison Talking Points

Use this framing when comparing with ex-skill, colleague-skill, or dot-skill projects:

| Question | Suggested Answer |
|---|---|
| Is this an ex simulator? | No. BondLens does not roleplay the other person or predict their inner state. |
| Is this a relationship advice bot? | Not generic advice. It requires chat evidence and should label uncertainty when data is thin. |
| Why not just ask ChatGPT? | BondLens forces action-card-first output, signal-ledger reasoning, confidence levels, counterevidence, alternative explanations, and safety boundaries. |
| What makes it privacy-friendly? | The Skill can work from pasted excerpts, but the CLI supports local redaction, segmentation, digest generation, and evidence indexing before upload. |
| What is the strongest demo? | A short synthetic chat excerpt that produces a low-pressure action card with evidence IDs and a ready-to-send message. |

## Content Priorities

1. Lead with the emotional hook, but immediately narrow the claim to evidence-backed action.
2. Show a concrete action-card demo above the fold.
3. Compare against persona simulation without dismissing those projects.
4. Make trust mechanisms visible: ledger, weighting, audit, confidence, counterevidence.
5. Keep safety boundaries explicit and prominent.
6. Link to installation and quickstart before deep workflow details.
7. Never use real private analyses as promotional examples; use synthetic excerpts only.
