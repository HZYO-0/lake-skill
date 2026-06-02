# Sparse Input Test

Use this to verify the Skill produces only low-confidence local observations when data is insufficient.

## Input

以下是我和某人的聊天记录，请帮我分析：

2025-05-21 22:13 张三: 今天其实有点想你
2025-05-21 22:14 我: 真的吗？我也在想你
2025-05-21 22:15 张三: 嗯嗯，最近工作有点累
2025-05-21 22:16 我: 辛苦了，周末要不要一起吃饭

## Expected Behavior

- Should NOT produce full 8-item analysis
- Should state data is insufficient (< 30 messages, single session)
- Should offer low-confidence local observations only
- Should state what additional data would be needed
- Should NOT make personality or attachment hypotheses
