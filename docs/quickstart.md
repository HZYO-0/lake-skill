# LakeSkill Quickstart

This guide shows three ways to run LakeSkill: quick paste, file upload, and privacy-first local preprocessing.

---

## 1. Quick Paste

Use this when you want a fast first read.

```text
使用 lake-skill，帮我分析这段聊天记录。我的目标是知道下一步怎么做。

[2026-06-01 22:13] 我: ...
[2026-06-01 22:14] 对方: ...
```

Best for:

- One specific moment
- A reply draft
- A low-confidence first impression

Limit: a short excerpt cannot support stable personality or relationship-pattern conclusions.

---

## 2. File Upload

Use this when you have enough messages for a real action card.

Supported inputs:

- TXT WeChat exports (from [WeChatDataAnalysis](https://github.com/LifeArchiveProject/WeChatDataAnalysis) or manual copy)
- CSV/TSV tables
- JSONL messages
- Plaintext SQLite databases (WeChatDataAnalysis decrypted DBs work directly)
- SRT/VTT voice transcripts
- OCR transcripts after text extraction

Prompt:

```text
使用 lake-skill，帮我分析这个聊天记录文件。
关系类型：暧昧/朋友/前任/伴侣/同事
当前状态：最近有点冷淡，我想知道下一步怎么做
```

Recommended data:

- 100+ messages
- Several days or weeks
- Both sides speaking
- Daily chat plus at least one tension, repair, help, or warm moment

---

## 3. Privacy-First Local Preprocessing

Use this when data is large or sensitive. Raw chat records stay local; you upload processed artifacts.

Install CLI:

```bash
git clone https://github.com/HZYO-0/lake-skill.git
cd lake-skill
pip install -e ".[dev]"
```

Initialize a project:

```bash
lake-skill init ./my_project
cd my_project
```

Put data under `input/`, then run one ingest command:

```bash
lake-skill ingest --file input/chat.csv --type csv --self-name 我 --target-name 对方 --out work/raw_messages.jsonl
```

For WeChat TXT:

```bash
lake-skill ingest --file input/chat.txt --type txt --self-name 我 --target-name 对方 --out work/raw_messages.jsonl
```

Then preprocess:

```bash
lake-skill redact --file work/raw_messages.jsonl --out work/messages.redacted.jsonl --privacy-mode cloud-safe
lake-skill segment --file work/messages.redacted.jsonl --out work/sessions.redacted.jsonl
lake-skill digest --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --out work/digest.redacted.md
lake-skill evidence --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --out work/evidence.redacted.jsonl
lake-skill export --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --out work/conversations.jsonl --mode conversations
```

Upload to the Skill:

- `work/digest.redacted.md`
- `work/sessions.redacted.jsonl`
- `work/evidence.redacted.jsonl`
- `work/conversations.jsonl`

Optional knowledge base:

```bash
lake-skill kb init --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --evidence work/evidence.redacted.jsonl --out kb/
```

Upload `kb/*.md` when asking for incremental updates.

---

## What A Good First Prompt Looks Like

```text
使用 lake-skill，帮我分析我和 TA 的聊天记录。

关系类型：暧昧但未确认
当前状态：最近对方回复变短，我担心自己踩雷
我想要：先给行动卡，再把完整报告写到文件
数据说明：这里是过去 3 周的聊天记录，包含日常、一次冲突、一次修复、几次求助
```

---

## Output Checklist

A complete 0.10.0 report should include:

- Relationship action card as the first screen
- Coverage declaration
- Evidence IDs for major claims
- Confidence, counterevidence, and alternative explanations
- Concrete next steps and ready-to-send messages
- Safety boundaries: no medical or mental-health judgement, no manipulation, no deterministic claims
