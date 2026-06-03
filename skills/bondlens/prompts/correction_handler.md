# BondLens Correction Handler

处理用户对分析结果的纠正。

## 处理流程

### 1. 理解纠正

收集以下信息：
- **场景**：用户指的是哪个具体场景/结论
- **错误**：分析中哪里不对
- **正确**：实际情况是什么
- **来源**：用户是怎么知道的（观察/对方告知/直觉）

### 2. 判断归属

将纠正归类到对应 Layer：
- Layer 0：核心互动规则
- Layer 1：关系背景
- Layer 2：对方表达 DNA
- Layer 3：自我表达 DNA
- Layer 4：互动模式
- Layer 5：依恋信号
- Layer 6：沟通建议

### 3. 生成 Correction 记录

```yaml
correction:
  id: COR-{timestamp}
  layer: {0-7}
  original: {原结论}
  corrected: {纠正后}
  source: user_observation | user_info | user_intuition
  confidence: high  # 用户纠正默认高置信度
  evidence_ids: [受影响的证据 ID]
```

### 4. 检查冲突

检查纠正是否影响其他结论：
- 直接影响：同一 Layer 的相关结论
- 间接影响：其他 Layer 的衍生结论
- 级联影响：基于被纠正结论的建议

### 5. 确认并写入

```
收到你的纠正。以下是更新计划：

直接更新：
- {结论} → {更新为}

级联更新（可能受影响）：
- {相关结论} → {建议更新为}（需要你确认）

确认？
```

## 重要原则

1. **不防御**：不试图证明原分析是对的
2. **优先用户**：用户比数据更了解对方
3. **降低置信度**：被纠正的结论及相关假设，置信度降低
4. **记录学习**：将纠正写入 update_log，供后续分析参考
