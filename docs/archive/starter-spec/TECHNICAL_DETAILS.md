# Technical Details

## 1. 标准消息 Schema

所有输入最终归一化为 `normalized_messages.jsonl`，每行一个 JSON object。

```json
{
  "message_id": "m_000001",
  "conversation_id": "wxid_target",
  "source_app": "wechat",
  "source_type": "sqlite",
  "timestamp": "2025-05-21T22:13:05+08:00",
  "sender_id": "wxid_xxx",
  "sender_role": "target",
  "receiver_role": "self",
  "message_type": "text",
  "modality": "text",
  "text": "今天其实有点想你",
  "text_redacted": "今天其实有点想你",
  "raw_text": "今天其实有点想你",
  "media": {
    "file_name": null,
    "duration_sec": null,
    "ocr_text": null,
    "asr_confidence": null,
    "ocr_confidence": null,
    "transcript_source": null
  },
  "conversation_context": {
    "is_group": false,
    "relationship_type": "ambiguous",
    "phase_hint": null
  },
  "source": {
    "file": "chat.db",
    "table": "messages",
    "row_id": 12345
  },
  "quality": {
    "parse_confidence": "high",
    "asr_confidence": null,
    "ocr_confidence": null,
    "timestamp_confidence": "high",
    "notes": []
  },
  "hash": "sha256:..."
}
```

## 2. Evidence Schema

```json
{
  "evidence_id": "E-20250521-003",
  "session_id": "S-20250521-001",
  "message_ids": ["m_000123"],
  "source_app": "wechat",
  "source_type": "voice_transcript",
  "message_type": "voice_transcript",
  "speaker": "target",
  "quote": "我不是不想回你，就是有时候不知道怎么说",
  "quote_redacted": "我不是不想回你，就是有时候不知道怎么说",
  "asr_confidence": 0.86,
  "ocr_confidence": null,
  "theme": ["关系压力", "解释困难", "回避沟通"],
  "supports": ["avoidance_signal", "conflict_delay"],
  "confidence": "medium",
  "alternative_explanations": ["工作压力", "表达能力限制", "当时情绪低"],
  "created_at": "2026-06-01T00:00:00+08:00"
}
```

## 3. Session Schema

```json
{
  "session_id": "S-20250521-001",
  "conversation_id": "wxid_target",
  "start": "2025-05-21T21:58:00+08:00",
  "end": "2025-05-21T23:20:00+08:00",
  "topic": "暧昧试探与情绪确认",
  "message_count": 48,
  "self_count": 27,
  "target_count": 21,
  "dominant_emotion": "亲近 + 不确定",
  "episode_type": ["ambiguous", "reassurance", "relationship_pressure"],
  "risk_level": "medium",
  "message_ids": ["m_000001", "m_000002"]
}
```

## 4. CLI 命令设计

命令名建议：`wri`。

### 4.1 初始化项目

```bash
wri init ./my_relationship_project
```

生成：

```text
input/
work/
kb/
reports/
config.yaml
```

### 4.2 检查输入

```bash
wri inspect input/chat.db --type sqlite
wri inspect input/chat.csv --type csv
wri inspect input/transcripts --type voice-transcript
```

### 4.3 导入 SQLite

```bash
wri ingest sqlite \
  --db input/chat.db \
  --conversation wxid_target \
  --self-id wxid_me \
  --target-id wxid_target \
  --schema-map config/schema_map.yaml \
  --out work/raw_messages.jsonl
```

### 4.4 导入 CSV/TXT/HTML

```bash
wri ingest csv --file input/chat.csv --self-name 我 --target-name 对方 --out work/raw_messages.jsonl
wri ingest txt --file input/chat.txt --format wechat-like --self-name 我 --target-name 对方 --out work/raw_messages.jsonl
wri ingest html --file input/chat.html --out work/raw_messages.jsonl
```

### 4.5 导入语音转文字

```bash
wri ingest voice-transcript \
  --file input/transcripts/voice.srt \
  --sender-role target \
  --conversation wxid_target \
  --out work/voice_messages.jsonl
```

批量导入：

```bash
wri ingest voice-transcript \
  --dir input/transcripts \
  --manifest input/voice_manifest.csv \
  --out work/voice_messages.jsonl
```

`voice_manifest.csv` 示例：

```csv
file,timestamp,sender_role,duration_sec,source_audio
voice_001.srt,2025-05-21T22:13:05+08:00,target,18.4,voice_001.mp3
voice_002.srt,2025-05-22T09:02:11+08:00,self,7.9,voice_002.mp3
```

### 4.6 导入 OCR

```bash
wri ingest ocr-transcript \
  --file input/ocr/chat_screenshot_001.jsonl \
  --out work/ocr_messages.jsonl
```

### 4.7 合并多源输入

```bash
wri merge \
  --in work/raw_messages.jsonl \
  --in work/voice_messages.jsonl \
  --in work/ocr_messages.jsonl \
  --out work/merged_messages.jsonl
```

### 4.8 归一化

```bash
wri normalize --in work/merged_messages.jsonl --out work/normalized_messages.jsonl
```

### 4.9 隐私处理

```bash
wri redact \
  --in work/normalized_messages.jsonl \
  --out work/normalized.cloud-safe.jsonl \
  --privacy-mode cloud-safe
```

### 4.10 会话切分与证据索引

```bash
wri segment --in work/normalized.cloud-safe.jsonl --out work/session_summaries.redacted.jsonl
wri digest --messages work/normalized.cloud-safe.jsonl --sessions work/session_summaries.redacted.jsonl --out work/relationship_digest.redacted.md
wri evidence --messages work/normalized.cloud-safe.jsonl --sessions work/session_summaries.redacted.jsonl --out work/evidence_index.redacted.jsonl
```

### 4.11 知识库

```bash
wri kb init --digest work/relationship_digest.redacted.md --evidence work/evidence_index.redacted.jsonl --out kb/
wri kb patch --old-kb kb/ --new-digest work/relationship_digest.redacted.md --new-evidence work/evidence_index.redacted.jsonl --out reports/kb_patch.md
```

## 5. SQLite schema 探测

不要假设微信数据库表名固定。必须实现 schema 探测：

```json
{
  "tables": [
    {
      "name": "messages",
      "columns": ["id", "talker", "sender", "timestamp", "type", "content"]
    }
  ],
  "candidate_message_tables": [
    {
      "table": "messages",
      "score": 0.91,
      "reason": ["has timestamp column", "has text/content column", "has sender/talker column"]
    }
  ]
}
```

用户可手动提供 `schema_map.yaml`：

```yaml
sqlite:
  message_table: messages
  columns:
    message_id: id
    conversation_id: talker
    sender_id: sender
    timestamp: create_time
    message_type: type
    text: content
  timestamp:
    unit: seconds
    timezone: Asia/Shanghai
```

## 6. 隐私模式

| 模式 | 适用 | 行为 |
|---|---|---|
| `local-raw` | 完全本地、不共享 | 不脱敏，强警告 |
| `local-safe` | 本地报告、低风险分享 | 脱敏手机号、身份证、地址、微信号等 |
| `cloud-safe` | 默认上传 ChatGPT Skill | 脱敏姓名、公司、学校、地址、微信号、精确金额等 |
| `publish-safe` | GitHub 示例、issue、fixture | 只允许合成数据，拒绝真实数据 |

## 7. 大数据处理

必须流式处理 JSONL，不要一次性读入全部聊天记录。

目标规模：

| 规模 | 目标 |
|---|---|
| 1,000 条 | 秒级 |
| 10,000 条 | 1 分钟内 |
| 100,000 条 | 可分块处理 |
| 500,000 条 | 不崩溃，提示分批 |

## 8. 低质量数据处理

ASR/OCR/截图转写必须进入 `quality` 字段，并影响置信度。

规则：

- `asr_confidence < 0.75`：最多中低置信。
- `ocr_confidence < 0.80`：最多低置信。
- 缺时间戳：不能用于回复间隔分析。
- 缺说话人：不能用于对方画像，只能用于上下文。
