# Input Formats

## Supported Formats

### CSV Files

**File extensions**: `.csv`, `.tsv`

**Column mappings**:
- Chinese: 时间, 日期, 发送者, 发送人, 接收者, 内容, 消息
- English: timestamp, time, date, sender, from, receiver, to, content, text, message

**Example**:
```csv
timestamp,sender,receiver,content
2025-05-21 22:13:05,张三,我,今天其实有点想你
2025-05-21 22:14:20,我,张三,真的吗？我也在想你
```

### TXT Files (WeChat Export)

**File extensions**: `.txt`, `.text`

**Format**: `YYYY-MM-DD HH:MM:SS 发送者: 内容`

**Example**:
```
2025-05-21 22:13:05 张三: 今天其实有点想你
2025-05-21 22:14:20 我: 真的吗？我也在想你
```

### SQLite Databases

**File extensions**: `.db`, `.sqlite`, `.sqlite3`

**Requirements**:
- Must be readable plaintext SQLite
- No encryption or key extraction
- User must have legitimate access

**Schema detection**: LakeSkill automatically detects message tables based on column names.

### Voice Transcripts

**File extensions**: `.srt`, `.vtt`, `.jsonl`, `.csv`

**SRT Example**:
```
1
00:00:00,000 --> 00:00:02,500
今天其实有点想你

2
00:00:03,000 --> 00:00:05,500
真的吗？我也在想你
```

**JSONL Example**:
```json
{"text": "今天其实有点想你", "timestamp": "2025-05-21T22:13:05", "asr_confidence": 0.9}
```

### OCR Transcripts

**File extensions**: `.jsonl`, `.csv`

**JSONL Example**:
```json
{"text": "今天其实有点想你", "timestamp": "2025-05-21T22:13:05", "ocr_confidence": 0.85}
```

## Data Quality

### Confidence Levels

- **high**: Parse confidence is high, timestamp is reliable
- **medium**: ASR/OCR confidence is moderate, timestamp may be approximate
- **low**: ASR/OCR confidence is low, timestamp is missing or unreliable

### Quality Fields

- `parse_confidence`: How well the message was parsed
- `asr_confidence`: Speech recognition confidence (0-1)
- `ocr_confidence`: OCR confidence (0-1)
- `timestamp_confidence`: How reliable the timestamp is
