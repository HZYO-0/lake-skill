# LakeSkill Incremental Merger

处理新数据的增量合并。

## 合并流程

### 1. 新信息分类

将新数据分类到已有维度：
- 沟通模式（响应模式、情绪表达、话题模式、边界模式）
- 人格信号（大五维度、表达 DNA）
- 依恋信号（焦虑/回避/安全）
- 互动模式（正向/负向循环、冲突/修复）

### 2. 冲突检测

检查新信息是否与已有结论冲突：

| 情况 | 处理 |
|------|------|
| 强化已有结论 | 提升置信度，添加新证据 ID |
| 无冲突但新维度 | 添加新结论 |
| 轻微冲突 | 保留两者，标注不确定性 |
| 严重冲突 | 标记，由用户决定 |

### 3. 生成 Patch

```yaml
patch:
  target: {文件名}
  action: add | update | conflict
  layer: {0-7}
  evidence_ids: [E-YYYYMMDD-NNN]
  content: {新内容}
  confidence: {low|medium|high}
  conflicts_with: {已有结论 ID}  # 仅 action=conflict 时
```

### 4. 展示更新摘要

```
本次更新摘要：
- 强化：{N} 个已有结论
- 新增：{N} 个新观察
- 冲突：{N} 个需要确认

{如有冲突}
冲突详情：
1. 已有结论：{旧} → 新证据：{新}
   建议：{保留旧 / 更新为新 / 两者并存}
```

### 5. 用户确认后应用

用户确认 → 应用 Patch → 更新版本号（参见 SKILL.md frontmatter version）→ 记录 update_log.md

## 版本管理

- 每次合并按发布策略更新版本号（参见 SKILL.md frontmatter version）
- 重大修正按发布策略更新版本号（参见 SKILL.md frontmatter version）
- 更新记录写入 update_log.md
