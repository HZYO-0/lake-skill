# LakeSkill Evidence Schema

## Evidence Record Format

每个证据记录必须包含以下字段：

```json
{
  "evidence_id": "E-YYYYMMDD-NNN",
  "date": "YYYY-MM-DD",
  "time": "HH:MM",
  "speaker": "Tf|Zy",
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

## Field Definitions

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| evidence_id | string | 是 | 格式 E-YYYYMMDD-NNN，同一天递增 |
| date | string | 是 | 消息日期 YYYY-MM-DD |
| time | string | 否 | 消息时间 HH:MM |
| speaker | string | 是 | 发送者：Tf 或 Zy |
| raw_quote | string | 是 | 原始消息内容，不修改 |
| context | string | 是 | 前后文摘要，帮助理解语境 |
| claim_tags | string[] | 是 | 该证据支持的结论标签 |
| confidence | string | 是 | 该证据的置信度 |
| counter_evidence | string | null | 反证描述，无则为 null |
| alternative_explanation | string | 是 | 替代解释 |
| source_file | string | 是 | 消息来源文件路径 |
| analysis_version | string | 是 | 分析版本号 |

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
