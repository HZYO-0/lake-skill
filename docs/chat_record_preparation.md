# Chat Record Preparation Guide

LakeSkill is only as good as the relationship evidence you provide. The goal is not to upload the largest possible archive; the goal is to provide enough representative scenes for the Skill to distinguish a one-off moment from a repeated pattern.

---

## How Much Data Is Enough?

| Data level | Minimum | Recommended use |
|---|---:|---|
| Tiny excerpt | 5-30 messages | Understand one reply, draft one message |
| Initial analysis | 30-100 messages | Identify tentative communication signals |
| Useful action card | 100+ messages across several days | Decide what to do this week |
| Full relationship report | Several weeks or months | Build profiles, interaction loops, playbook, uncertainty layer |

If you only provide a short excerpt, LakeSkill should mark conclusions as low confidence and avoid stable personality or attachment claims.

---

## Scene Coverage Matters More Than Raw Count

Try to include several of these scenes:

| Scene | Why it matters |
|---|---|
| Daily baseline chat | Normal rhythm, tone, response length |
| Help-seeking | Trust, practical closeness, reciprocity |
| Warm moments | Affection, safety, approach signals |
| Delayed or short replies | Withdrawal, boundaries, workload, uncertainty |
| Conflict or pressure | Escalation path and stress behavior |
| Repair or apology | Whether the relationship can recover |
| Boundary discussions | What not to push |
| Future plans or invitations | Initiative and investment |

For a first full report, aim for at least 3-5 scene types.

---

## Three Import Paths

### A. Paste Chat Records

Fastest path for testing.

```text
以下是我和某人的聊天记录，请用 LakeSkill 分析：

2026-06-01 22:13 我: 今天有点不知道怎么接她的话
2026-06-01 22:14 对方: ...
```

Use this for short excerpts, reply drafts, and low-confidence local observations.

### B. Upload A File

Use this for longer records.

Supported formats:

- TXT
- CSV/TSV
- JSONL
- Plaintext SQLite
- SRT/VTT transcripts
- OCR text outputs

CSV should include timestamp, sender, and content columns. TXT should preserve timestamps and speaker names where possible.

### C. Local Preprocessing

Use this for privacy-sensitive or large datasets. Raw data stays local; only redacted artifacts are uploaded.

```bash
lake-skill ingest --file input/chat.csv --type csv --self-name 我 --target-name 对方 --out work/raw_messages.jsonl
lake-skill redact --file work/raw_messages.jsonl --out work/messages.redacted.jsonl --privacy-mode cloud-safe
lake-skill segment --file work/messages.redacted.jsonl --out work/sessions.redacted.jsonl
lake-skill digest --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --out work/digest.redacted.md
lake-skill evidence --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --out work/evidence.redacted.jsonl
lake-skill export --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --out work/conversations.jsonl --mode conversations
```

Upload:

- `work/digest.redacted.md`
- `work/sessions.redacted.jsonl`
- `work/evidence.redacted.jsonl`
- `work/conversations.jsonl`

---

## Context To Provide With The Data

Add a short intake note:

```text
关系类型：
当前状态：
双方称呼：
我最想知道：
最近典型场景：
数据时间范围：
是否需要先给行动卡：
```

This prevents the agent from guessing the relationship context.

---

## Privacy And Safety

Do not upload data you do not have permission to use. LakeSkill does not decrypt databases, bypass access controls, or infer hidden intent with certainty.

Before uploading to a cloud model, consider removing:

- Real names
- Phone numbers
- Addresses
- Account IDs
- Private third-party details
- Financial, medical, or legal identifiers

Use `cloud-safe` redaction when possible.
