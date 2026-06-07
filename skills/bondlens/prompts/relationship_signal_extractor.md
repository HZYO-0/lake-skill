# BondLens Relationship Signal Extractor

在任何关系判断、人格画像、行动建议之前，先生成关系信号台账。台账是后续所有强结论的输入；未进入台账的关键关系信号不得用于暗中推理。

## 输出文件

- `relationship_signal_ledger.jsonl`: 机器可审计台账
- `relationship_signal_ledger.md`: 给用户或审阅者看的摘要
- `contradiction_ledger.md`: 冲突、摇摆、反证和用户纠正

## 必扫 T1 信号

T1 是最高权重关系信号，必须单独扫描并全部列出：

| 类型 | 例子 | 处理 |
|------|------|------|
| 表白/推进 | "我喜欢你"、"我想争取" | 记录原话、回应、后续行为 |
| 拒绝/暂停 | "不合适"、"现在做不出发展" | 不直接推出"完全不喜欢" |
| 条件性接受 | "以后再看"、"如果我想法明确了" | 作为开放条件，不归类为拒绝 |
| 关系定义 | "我们什么关系"、"朋友/对象" | 记录双方定义是否一致 |
| 边界/雷区 | "控制欲强"、"不要这样" | 连接到行动禁忌 |
| 自我认知 | "我是回避型"、"我不配" | 作为自我陈述，不当作临床诊断 |
| 未来时间线 | "过年后"、"毕业后" | 记录条件、时间、是否兑现 |
| 矛盾/摇摆 | "说不出完全不可能" | 放入反证台账 |

## JSONL 字段

每条记录必须包含：

```json
{
  "evidence_id": "E-YYYYMMDD-NNN",
  "date": "YYYY-MM-DD",
  "speaker": "self|target|other",
  "tier": "T1|T2|T3|T4",
  "signal_type": "confession|rejection|conditional_acceptance|relationship_definition|boundary|self_understanding|future_timeline|ambivalence|conflict|repair|behavior_pattern|daily_context",
  "quote": "原话或用户口述摘要",
  "local_context": "这句话前后发生了什么",
  "later_followup": "后续是否靠近、疏远、修复或改口",
  "interpretation_candidates": ["解释 A", "解释 B"],
  "counterevidence_ids": ["E-YYYYMMDD-NNN"],
  "source": "chat_record|user_context|user_correction",
  "confidence": "low|medium|high"
}
```

## 提取规则

1. T1 全量提取，不受时间衰减影响。
2. T2 提取所有情绪转折、冲突、修复和关系暴露后的行为。
3. T3 只记录重复模式，每个模式附 2-3 条代表性证据。
4. T4 只做统计和语言风格背景，不生成关系结论。
5. 用户纠正默认进入 `source=user_correction`，并触发重跑台账和主结论。

## 禁止误判

- 一次拒绝不得自动推出"完全没可能"。
- 自称回避型不得自动推出"就是回避型"。
- 高频日常聊天不得自动推出"关系稳定/有好感"。
- 条件性接受不得被合并进普通拒绝。
- 后续行为与早期表态冲突时，必须写入 `contradiction_ledger.md`。
