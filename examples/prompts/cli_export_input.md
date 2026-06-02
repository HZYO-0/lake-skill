# CLI Export Input Test

Use this to verify the Skill correctly processes CLI-preprocessed data (digest + evidence index + session summaries).

## Input

以下是我通过本地预处理工具生成的聊天摘要和证据索引，请帮我分析：

### 摘要（digest.redacted.md）

## 关系统计
- 分析时间范围：2025-04-01 至 2025-05-10
- 总消息数：52 条
- 会话数：10 个
- 对方消息：22 条，我方消息：30 条
- 平均回复时间：对方 8.5 分钟，我方 2.1 分钟

## 时间趋势
- 对方回复时间呈上升趋势（从 2 分钟增加到 15 分钟）
- 我方消息长度保持稳定
- 会话频率略有下降

### 证据索引（evidence_index.redacted.jsonl）

```jsonl
{"evidence_id": "E001", "theme": "情感表达", "quote": "今天其实有点想你", "session_id": "S001", "speaker": "对方", "confidence": "high"}
{"evidence_id": "E002", "theme": "回避", "quote": "再说吧，最近有点累", "session_id": "S003", "speaker": "对方", "confidence": "medium"}
{"evidence_id": "E003", "theme": "回避", "quote": "不想出门", "session_id": "S005", "speaker": "对方", "confidence": "medium"}
{"evidence_id": "E004", "theme": "关系压力", "quote": "我觉得我们之间有点问题", "session_id": "S010", "speaker": "对方", "confidence": "high"}
{"evidence_id": "E005", "theme": "回避", "quote": "算了，以后再说吧", "session_id": "S010", "speaker": "对方", "confidence": "high"}
{"evidence_id": "E006", "theme": "修复", "quote": "没关系，慢慢说", "session_id": "S010", "speaker": "我方", "confidence": "medium"}
{"evidence_id": "E007", "theme": "情感表达", "quote": "你说的我都记得", "session_id": "S008", "speaker": "我方", "confidence": "high"}
{"evidence_id": "E008", "theme": "边界", "quote": "看情况吧", "session_id": "S007", "speaker": "对方", "confidence": "low"}
```

### 会话摘要（session_summaries.redacted.jsonl）

```jsonl
{"session_id": "S001", "start": "2025-04-01T09:15:00", "message_count": 4, "dominant_theme": "日常分享"}
{"session_id": "S003", "start": "2025-04-10T22:00:00", "message_count": 4, "dominant_theme": "回避"}
{"session_id": "S010", "start": "2025-05-10T22:30:00", "message_count": 8, "dominant_theme": "关系压力"}
```

## Expected Behavior

- Should reference evidence IDs (E001, E002, etc.) in analysis
- Should use session IDs to contextualize observations
- Should acknowledge data was CLI-preprocessed
- Should proceed with full analysis (data is sufficient)
- Should cite specific quotes from evidence index
- Should produce confidence-calibrated hypotheses
