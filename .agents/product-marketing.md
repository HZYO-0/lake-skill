# Product Marketing Context

*Last updated: 2026-06-17*

## Product Overview

**One-liner:** LakeSkill 湖镜 turns relationship chat records into evidence-backed action cards instead of confident guesses.

**What it does:** LakeSkill is an agent Skill plus optional local CLI for intimate relationship chat analysis. It organizes chat evidence into timelines, signal ledgers, confidence labels, counterevidence, alternative explanations, data-readiness checks, and practical next-step cards. It does not pretend to be the other person, simulate a partner, promise outcomes, or provide medical or mental-health judgement.

**Product category:** Agent Skill, privacy-first chat analysis, relationship communication coaching, local preprocessing CLI.

**Product type:** Open-source Skill package and CLI.

**Business model:** Open-source adoption first; future services may include privacy-first data preparation, local setup, report templates, and workflow support.

## Target Audience

**Target users:** Developers and agent users who work with Codex, Claude Code, OpenCode, or similar runtimes; Chinese content-platform users who want safer relationship chat analysis; privacy-sensitive users with large chat exports.

**Primary use case:** Understand what relationship chat evidence supports, what it does not support, and what low-risk action to take next.

**Jobs to be done:**

- Turn messy relationship chats into a concise action card.
- Check whether the data is enough for local observation, action-card output, or a full report.
- Prepare redacted, upload-ready artifacts before using an AI agent.
- Create public-safe demos for GitHub, Xiaohongshu, and Douyin without exposing real chats.

## Problems & Pain Points

**Core problem:** People often paste emotionally sensitive chats into AI and receive overconfident interpretations that feel certain but are not evidence-bound.

**Why alternatives fall short:**

- Generic chatbots can mirror anxiety and produce confident answers without evidence IDs.
- Persona simulation can blur the line between analysis and emotional dependency.
- Manual review is slow and easy to bias toward one dramatic message.
- Large raw exports are risky to upload without local redaction and readiness checks.

**Emotional tension:** Users want an answer, but the safer answer is often “the evidence only supports a smaller, lower-risk action.”

## Differentiation

**Key differentiators:**

- Action card first, long report second.
- Evidence ledger before conclusions.
- T1-T4 signal weighting and timeline-first interpretation.
- Doctor readiness tiers: 只能局部观察 / 可出行动卡 / 可出完整报告.
- Local redaction, digest, evidence index, and upload bundle.
- Synthetic demo generation for public promotion.
- Explicit boundaries against persona simulation, dependency, manipulation, and outcome promises.

**Why this is better:** The user gets a practical next step while still seeing the limits of the evidence.

## Objections

| Objection | Response |
|---|---|
| “Is this just another relationship chatbot?” | No. LakeSkill does not roleplay the other person; it organizes evidence and labels confidence. |
| “Is it safe to upload chats?” | The recommended path is local preprocessing, redaction, doctor checks, and bundle creation before upload. |
| “Can it tell me what TA really feels?” | No. It can only say what the chat evidence supports, what it does not support, and what to do next with lower risk. |
| “Is it too technical?” | Non-technical users can paste short snippets; technical and privacy-sensitive users can use the CLI. |

**Anti-persona:** Users seeking certainty, manipulation tactics, relationship outcome guarantees, clinical labels, or simulated companionship.

## Customer Language

**How they describe the problem:**

- “TA 回得慢，是不是不在乎？”
- “聊天记录太多，我不知道哪些才是关键。”
- “AI 说得太肯定，我反而更上头。”
- “我想知道下一句怎么说，但不想逼对方。”

**Words to use:** 证据、行动卡、置信度、反证、替代解释、本地脱敏、数据体检、低风险下一步、合成示例、湖镜。

**Words to avoid:** outcome promises, certainty about hidden inner states, manipulation tactics, clinical labels, real private chats as examples.

## Brand Voice

**Tone:** Calm, direct, evidence-first, privacy-aware.

**Style:** Chinese-first for public promotion, concise for GitHub, practical rather than therapeutic or sensational.

**Personality:** Quiet, grounded, careful, useful, humane.

## Proof Points

**Value themes:**

| Theme | Proof |
|---|---|
| Evidence-first | Evidence IDs, signal ledger, reliability audit |
| Privacy-first | Redact, check-leaks, doctor, bundle |
| Public-safe promotion | `lake-skill demo` and synthetic `social_assets/` |
| Practical action | Lake-mirror action card before long report |

## Goals

**Business goal:** Drive GitHub/Skill installs first, then Chinese content-platform awareness, then privacy-first service exploration.

**Conversion action:** Install the Skill, run `lake-skill demo`, or use the local preprocessing CLI.

**Current metrics:** Not established.
