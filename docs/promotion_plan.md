# LakeSkill 湖镜 Promotion Plan

## Positioning

LakeSkill should be presented as a calm relationship mirror for chat evidence, not as a partner simulator, ex simulator, or generic advice bot.

Core positioning:

```text
不是替你求一个答案，而是先陪你看清水面。
```

Short Chinese launch line:

```text
LakeSkill 湖镜：把聊天记录放到一面安静的湖上，看见关系的倒影，也看见自己的心。
```

Short English launch line:

```text
LakeSkill is a calm relationship mirror for chat evidence, action cards, uncertainty, and safer next messages.
```

## GitHub Setup

Recommended GitHub About description:

```text
A calm relationship mirror for chat evidence: action cards, signal ledgers, reliability audits, and privacy-first local preprocessing.
```

Recommended repository topics:

```text
ai-skill
agent-skills
relationship-analysis
chat-analysis
privacy-first
evidence-based
codex
claude-code
wechat
communication-coaching
```

## Skill Directory Listing

Title:

```text
LakeSkill 湖镜 - A Calm Relationship Mirror
```

Short description:

```text
Turn relationship chat records into evidence-backed action cards, confidence-labeled interpretations, and ready-to-send messages.
```

Long description:

```text
LakeSkill is an agent Skill for analyzing intimate relationship chat records without pretending to be the other person. It reads pasted chats or locally preprocessed exports, builds a relationship signal ledger, checks evidence sufficiency, and produces a lake-mirror action card before the full report. Outputs include what to do this week, what not to overclaim, ready-to-send messages, confidence levels, counterevidence, alternative explanations, and safety boundaries. For sensitive or large datasets, the optional CLI can redact, segment, summarize, and index evidence locally before upload.
```

Key differentiators:

- Lake-mirror action card first, long report second
- Evidence ledger before conclusions
- T1-T4 signal weighting and timeline-first interpretation
- Reliability audit for overclaims and missing counterevidence
- Privacy-first local preprocessing CLI
- Explicit refusal of diagnosis, manipulation, and persona simulation

## Launch Posts

Chinese post:

```text
我做了一个新的 agent skill：LakeSkill 湖镜。

它不是前任模拟器，也不是让 AI 猜 TA 爱不爱你。

它更像一面湖：把聊天记录、关键事件和你的感受放到一个安静的水面上，让你看见关系里的信号，也看见自己的心。

它先给一张湖镜行动卡：

- 现在是什么局势
- 本周怎么做
- 哪些判断不能过度解读
- 哪些雷别踩
- 下一句话怎么发

核心机制是 evidence first：先建关系信号台账，再做判断；每个主要结论尽量给证据、置信度、反证和替代解释。

不是替你求一个答案，而是先陪你看清水面。

安装：
npx skills add HZYO-0/lake-skill -y
```

English post:

```text
I built LakeSkill, an agent Skill for evidence-based relationship chat analysis.

It is not a partner simulator, an ex simulator, or a persona replay tool.

It works more like a calm lake surface: place the chat evidence there, then look at the reflection with less panic and more structure.

It starts with a lake-mirror action card:

- what is happening now
- what to do this week
- what not to overclaim
- what not to say
- what message to send next

The workflow is evidence first: build a relationship signal ledger, weight key signals, check uncertainty, and then generate the action card and full report. For sensitive datasets, the optional CLI can redact, segment, summarize, and index evidence locally before upload.

Install:
npx skills add HZYO-0/lake-skill -y
```

## Comparison Talking Points

| Question | Suggested Answer |
|---|---|
| Is this an ex simulator? | No. LakeSkill does not roleplay the other person or predict their inner state. |
| Is this a relationship advice bot? | Not generic advice. It requires chat evidence and should label uncertainty when data is thin. |
| Why not just ask ChatGPT? | LakeSkill forces action-card-first output, signal-ledger reasoning, confidence levels, counterevidence, alternative explanations, and safety boundaries. |
| What makes it privacy-friendly? | The Skill can work from pasted excerpts, but the CLI supports local redaction, segmentation, digest generation, and evidence indexing before upload. |
| What is the strongest demo? | A short synthetic chat excerpt that produces a low-pressure lake-mirror action card with evidence IDs and a ready-to-send message. |

## Content Priorities

1. Lead with the lake/mirror emotional hook, then narrow the claim to evidence-backed action.
2. Show a concrete lake-mirror action-card demo above the fold.
3. Compare against persona simulation without dismissing those projects.
4. Make trust mechanisms visible: ledger, weighting, audit, confidence, counterevidence.
5. Keep safety boundaries explicit and prominent.
6. Link to installation and quickstart before deep workflow details.
7. Never use real private analyses as promotional examples; use synthetic excerpts only.
