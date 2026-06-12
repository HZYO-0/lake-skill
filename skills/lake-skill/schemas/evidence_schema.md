# LakeSkill Evidence Schema

## 两种证据格式

LakeSkill 有两种证据记录格式，用途不同：

| 格式 | 文件 | 用途 |
|------|------|------|
| **Evidence Index** | `evidence_index.jsonl` | 通用证据索引，供报告引用 |
| **Signal Ledger** | `relationship_signal_ledger.jsonl` | 关系信号台账，供行动卡和人格画像使用 |

两种格式共享 `evidence_id`，可互相引用。

---

## Evidence Index 格式（evidence_index.jsonl）

```json
{
  "evidence_id": "E-YYYYMMDD-NNN",
  "date": "YYYY-MM-DD",
  "time": "HH:MM",
  "speaker": "{target_name}|{self_name}",
  "raw_quote": "原始消息内容",
  "context": "前后文摘要（2-3 句）",
  "claim_tags": ["tag1", "tag2"],
  "confidence": "low|medium|high",
  "counter_evidence": "反证描述或 null",
  "alternative_explanation": "替代解释",
  "source_file": "消息来源文件路径",
  "analysis_version": "0.10.0"
}
```

### Field Definitions

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| evidence_id | string | 是 | 格式 E-YYYYMMDD-NNN，同一天递增 |
| date | string | 是 | 消息日期 YYYY-MM-DD |
| time | string | 否 | 消息时间 HH:MM |
| speaker | string | 是 | 发送者：`{target_name}` 或 `{self_name}` |
| raw_quote | string | 是 | 原始消息内容，不修改 |
| context | string | 是 | 前后文摘要，帮助理解语境 |
| claim_tags | string[] | 是 | 该证据支持的结论标签 |
| confidence | string | 是 | 该证据的置信度 |
| counter_evidence | string \| null | 否 | 反证描述，无则为 null |
| alternative_explanation | string | 是 | 替代解释 |
| source_file | string | 是 | 消息来源文件路径 |
| analysis_version | string | 是 | 分析版本号 |

---

## Signal Ledger 格式（relationship_signal_ledger.jsonl）

由 `prompts/relationship_signal_extractor.md` 生成，用于 T1-T4 信号分层。

```json
{
  "evidence_id": "E-YYYYMMDD-NNN",
  "date": "YYYY-MM-DD",
  "speaker": "self|target|other",
  "tier": "T1|T2|T3|T4",
  "signal_type": "confession|rejection|conditional_acceptance|...",
  "quote": "原话或用户口述摘要",
  "local_context": "这句话前后发生了什么",
  "later_followup": "后续是否靠近、疏远、修复或改口",
  "interpretation_candidates": ["解释 A", "解释 B"],
  "counterevidence_ids": ["E-YYYYMMDD-NNN"],
  "source": "chat_record|user_context|user_correction",
  "confidence": "low|medium|high"
}
```

### 字段映射

| Signal Ledger | Evidence Index | 说明 |
|---------------|---------------|------|
| quote | raw_quote | 原话内容 |
| local_context | context | 前后文 |
| counterevidence_ids | counter_evidence | 反证（ID 列表 vs 文字描述） |
| tier | — | 信号分层（T1-T4） |
| signal_type | claim_tags | 信号类型 vs 结论标签 |
| source | source_file | 数据来源类型 vs 文件路径 |

## Claim Tags

| Tag | 说明 |
|-----|------|
| attachment-avoidant | 回避型依恋信号 |
| attachment-anxious | 焦虑型依恋信号 |
| attachment-secure | 安全型依恋信号 |
| boundary-explicit | 显性边界 |
| boundary-implicit | 隐性边界 |
| conflict-escalation | 冲突升级 |
| conflict-repair | 冲突修复 |
| expression-nonliteral | 非字面表达 |
| expression-emotional | 情绪表达 |
| pattern-approach | 亲近行为 |
| pattern-withdraw | 疏远行为 |
| pattern-communication | 沟通模式 |
| persona-hard-rule | 硬规则 |
| persona-identity | 身份定位 |
| persona-expression | 表达风格 |
| persona-decision | 决策模式 |
| persona-relationship | 关系行为 |
| persona-boundary | 边界红线 |
| turning-point | 关键转折点 |

## File Location

证据索引文件位于分析目录下：
```
analyses/{relationship}/evidence_index.jsonl
```

每个分析报告必须引用此索引中的证据 ID。
