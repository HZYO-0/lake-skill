# Architecture

## 1. 总体架构

```text
┌────────────────────────────────────────────────────────────┐
│ Raw Inputs                                                  │
│ WeChat SQLite / CSV / TXT / HTML / JSONL / ASR / OCR        │
└────────────────────────────────────────────────────────────┘
                         ↓ local only
┌────────────────────────────────────────────────────────────┐
│ Local CLI Preprocessing                                     │
│ inspect → ingest → normalize → redact → segment → evidence  │
└────────────────────────────────────────────────────────────┘
                         ↓ cloud-safe output
┌────────────────────────────────────────────────────────────┐
│ Upload-safe Artifacts                                       │
│ digest.redacted.md / sessions.redacted.jsonl / evidence      │
└────────────────────────────────────────────────────────────┘
                         ↓ user uploads to ChatGPT
┌────────────────────────────────────────────────────────────┐
│ ChatGPT Skill                                                │
│ profile report / attachment hypotheses / communication plan │
└────────────────────────────────────────────────────────────┘
                         ↓
┌────────────────────────────────────────────────────────────┐
│ Relationship Knowledge Base                                 │
│ kb/*.md + evidence_index.jsonl + update_log.md              │
└────────────────────────────────────────────────────────────┘
```

## 2. 推荐仓库结构

```text
wechat-relationship-insight/
├── README.md
├── LICENSE
├── SECURITY.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── .gitignore
├── pyproject.toml
├── Makefile
├── Dockerfile
├── docker-compose.yml
│
├── skill/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── scripts/
│   │   ├── validate_input.py
│   │   ├── inspect_sqlite_schema.py
│   │   ├── ingest_wechat_sqlite.py
│   │   ├── ingest_csv.py
│   │   ├── ingest_txt.py
│   │   ├── ingest_html.py
│   │   ├── ingest_voice_transcript.py
│   │   ├── ingest_ocr_transcript.py
│   │   ├── normalize_messages.py
│   │   ├── redact_pii.py
│   │   ├── segment_sessions.py
│   │   ├── build_digest.py
│   │   ├── build_evidence_index.py
│   │   └── update_kb_patch.py
│   ├── references/
│   │   ├── input_formats.md
│   │   ├── normalized_schema.md
│   │   ├── media_transcript_schema.md
│   │   ├── local_vs_cloud_privacy.md
│   │   ├── output_templates.md
│   │   └── frameworks/
│   │       ├── evidence_ladder.md
│   │       ├── big_five_communication_signals.md
│   │       ├── attachment_anxiety_avoidance.md
│   │       ├── relationship_communication_patterns.md
│   │       ├── symbolic_mode_policy.md
│   │       └── forbidden_overclaims.md
│   └── assets/
│       ├── report_template.md
│       ├── communication_playbook_template.md
│       └── kb_template/
│
├── cli/
│   └── wechat_relationship_insight/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       ├── schema.py
│       ├── adapters/
│       ├── privacy/
│       ├── media/
│       ├── segmentation/
│       ├── evidence/
│       ├── kb/
│       └── reports/
│
├── tests/
│   ├── fixtures/
│   ├── unit/
│   ├── integration/
│   ├── safety/
│   └── golden/
│
├── examples/
│   ├── synthetic_input/
│   ├── synthetic_outputs/
│   └── prompts/
│
├── docs/
│   ├── quickstart.md
│   ├── local_deployment.md
│   ├── chatgpt_skill_deployment.md
│   ├── input_database_policy.md
│   ├── media_transcripts.md
│   ├── privacy_model.md
│   ├── threat_model.md
│   ├── output_interpretation.md
│   ├── testing_strategy.md
│   └── release_checklist.md
│
└── .github/
    └── workflows/
        ├── ci.yml
        ├── security.yml
        ├── package-skill.yml
        └── release.yml
```

## 3. 模块职责

### 3.1 adapters

把不同来源的数据转成统一 raw message：

- `wechat_sqlite.py`
- `wechat_csv.py`
- `wechat_txt.py`
- `wechat_html.py`
- `generic_jsonl.py`
- `voice_transcript.py`
- `ocr_transcript.py`
- `manual_markdown.py`

### 3.2 normalize

把 raw message 转成标准 schema：

```text
message_id
conversation_id
source_app
source_type
timestamp
sender_role
message_type
modality
text
media
quality
source
hash
```

### 3.3 privacy

实现四种 privacy mode，并提供 leakage checker。

### 3.4 segmentation

按时间间隔、话题变化、情绪变化、冲突/修复、复联、冷淡、暧昧升温等切分会话。

### 3.5 evidence

把关键证据编号化，生成 evidence index。

### 3.6 reports

生成本地可上传的摘要：

- `relationship_digest.redacted.md`
- `session_summaries.redacted.jsonl`
- `metrics.json`

### 3.7 kb

管理长期知识库：

- 初始化 KB。
- 增量 patch。
- 置信度更新。
- 反证合并。
- `update_log.md`。

## 4. Skill 职责

Skill 不负责解密、复杂 OCR/ASR 或数据库破解。Skill 负责：

- 读取 digest、sessions、evidence、旧 KB。
- 生成证据型报告。
- 进行非临床人格/依恋信号分析。
- 输出沟通建议和消息草稿。
- 生成 `kb_patch.md`。

## 5. 本地 CLI 与 Skill 的分工

| 层 | 本地 CLI | ChatGPT Skill |
|---|---|---|
| 数据读取 | 是 | 可选，不推荐原始上传 |
| 数据库 schema 探测 | 是 | 否 |
| 语音/OCR 转写结果导入 | 是 | 只分析转写文本 |
| 脱敏 | 是 | 检查与提醒 |
| 会话切分 | 是 | 可二次解释 |
| 证据索引 | 是 | 引用 evidence_id |
| 人格/依恋报告 | 可用本地 LLM | 默认由 Skill 做 |
| 沟通建议 | 可用本地 LLM | 默认由 Skill 做 |
| KB patch | 本地结构化辅助 | 默认由 Skill 做 |
