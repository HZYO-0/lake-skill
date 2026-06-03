# BondLens Report Builder

生成 8 层结构的 BondLens 分析报告。

## 报告结构

### Layer 0: 核心互动规则

从数据中提炼 3-5 条最重要的互动规则。

格式：
```
规则名称：{name}
证据：{IDs}
置信度：{level}
描述：{description}
```

### Layer 1: 关系背景

- 关系时间线（关键阶段划分）
- 当前状态
- 关系演变趋势

### Layer 2: 对方表达 DNA

基于 `persona_analyzer.md` 的 Target Profile 输出。

### Layer 3: 我的表达 DNA

基于 `persona_analyzer.md` 的 Self Profile 输出。

### Layer 4: 互动模式

基于 `interaction_analyzer.md` 输出。

### Layer 5: 依恋信号

基于 `attachment_analyzer.md` 输出。

### Layer 6: 沟通建议

分为：
- **日常聊天**：话题建议 + 示例
- **暧昧推进**（如适用）：低压力增进方式
- **冲突修复**：具体修复语言
- **边界表达**：如何表达个人边界
- **消息草稿**：多语气版本（温和/直接/降压/有边界）

### Layer 7: 不确定性说明

列出所有分析的：
- 低置信度结论
- 缺失的反证
- 替代解释
- 需要更多数据验证的假设

## 证据引用规范

每个主要结论必须：
1. 引用证据 ID（E-YYYYMMDD-NNN 格式）
2. 标注置信度（低/中/高）
3. 提供反证或说明无强反证
4. 提供至少 1 个替代解释

## 语言规范

使用：
> 聊天记录呈现某些……信号。该判断置信度为……。替代解释包括……。

禁止：
> 对方就是……型。
> 对方一定……。
> 这能让对方离不开你。

## 输出格式

```markdown
# BondLens 关系分析报告

**分析对象**: {self_name} ↔ {target_name}
**数据范围**: {date_range}
**总消息量**: {total_messages}
**分析日期**: {analysis_date}

---

## Layer 0: 核心互动规则
{3-5 条规则}

## Layer 1: 关系背景
{时间线 + 当前状态}

## Layer 2: {target_name} 表达 DNA
{Target Profile}

## Layer 3: {self_name} 表达 DNA
{Self Profile}

## Layer 4: 互动模式
{正向/负向循环 + 冲突/修复路径}

## Layer 5: 依恋信号
{双方依恋假设}

## Layer 6: 沟通建议
{分类建议 + 消息草稿}

## Layer 7: 不确定性说明
{低置信度 + 替代解释}

---

## 附录
- A: 消息量统计
- B: 证据索引
```
