---
name: bondlens
description: "Evidence-based intimate relationship chat analysis. Generates action briefs (what to do this week, what to avoid, ready-to-send messages), personality profiles with quote anchoring, interaction pattern analysis, attachment hypotheses with evidence IDs, confidence levels, and alternative explanations. Provides coaching, message drafts, and incremental knowledge base updates."
argument-hint: "[分析|教练|更新]"
version: "0.9.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

# BondLens 关系镜

Evidence-based intimate relationship chat analysis.

## 激活条件

**激活当**：
- 用户粘贴或上传聊天记录并要求分析
- 用户说 `/bondlens` 或 "帮我分析一下我们的聊天记录"
- 用户问 "我该怎么说" 或 "下一步怎么办"（关系上下文）
- 用户提供 CLI 预处理产物并要求解读
- 用户想要基于证据的沟通教练

**不激活当**：
- 用户问一般性关系建议但没有提供数据
- 用户要求解密数据库
- 用户要求临床诊断（"他是不是回避型人格"）
- 用户要求操控策略（PUA、情感勒索、嫉妒诱导）
- 用户问非关系话题

## 工具使用规则

| 任务 | 工具 |
|------|------|
| 读取用户上传的文件 | Read |
| 读取聊天记录文件（CSV/TXT/JSONL/SQLite） | Read |
| 写入分析报告 | Write |
| 更新知识库 | Edit |
| 运行 CLI 工具（可选） | Bash |

## 工作流

### Step 0: 确认关系类型、分析目标与工作模式

参考 `prompts/intake.md`，在 3 轮对话内收集：

1. **基本信息**：关系类型、当前状态、双方称呼、时长
2. **典型场景**：一个最近的互动场景
3. **数据来源**：能提供什么数据
4. **工作模式**（必选）：

| 模式 | 适用场景 | 输出风格 |
|------|---------|---------|
| `support` | 情感支持 | 先共情，再给建议，语气温和 |
| `practical` | 实操建议 | 先判断，再给动作，语气直接 |
| `repair` | 关系修复 | 先分析冲突，再给修复步骤，语气谨慎 |
| `auto` | 默认 | 根据用户消息自动判断 |

每轮可跳过。收集完毕后展示确认汇总。

```
信息汇总：
  关系类型：{type}
  当前状态：{status}
  你的称呼：{self_name}
  对方称呼：{target_name}
  时长：{duration}
  数据来源：{source}
  典型场景：{scene_summary}
  工作模式：{mode}

确认？（确认 / 修改 [字段名]）
```

**CLI 快捷路径**：如果用户通过 CLI 生成了 `bondlens_intake.yaml`，直接读取该文件跳过收集轮次。如果缺少 intake 文件，按上述流程收集后生成 `bondlens_intake.yaml` + `bondlens_intake.md`。

### Step 1: 数据导入

根据用户提供的数据类型，选择处理方式：

**方式 A: 直接粘贴聊天记录**
- 解析时间戳、发送者、消息内容
- 标准化为内部格式

**方式 B: 上传文件**
- CSV/TXT：自动检测列映射
- JSONL：直接读取结构化数据
- SQLite：使用 SQLite 适配器（支持 WeChatMsg/PyWxDump 导出格式）
- PDF/图片：OCR 提取文本

**方式 C: CLI 预处理产物**
- digest.md + evidence.jsonl + sessions.jsonl
- 直接进入分析阶段

**方式 D: 增量更新**
- 已有知识库 + 新数据
- 参考 `prompts/merger.md` 执行增量合并

### Step 2: 数据充分性评估

参考 `prompts/data_assessment.md`，评估：

| 维度 | 不足 | 基本 | 充分 |
|------|------|------|------|
| 消息量 | <30 条 | 30-100 条 | 100+ 条 |
| 时间跨度 | <1 天 | 1-7 天 | 1+ 周 |
| 双方参与 | 只有一方 | 严重不平衡 | 基本均衡 |
| 场景多样性 | 只有闲聊 | 有冲突 | 冲突+修复 |

- **充分** → 进入完整分析
- **基本** → 分析但标注低置信维度
- **不足** → 仅输出局部观察，提示补充数据

### Step 3: 分析执行

**3a: 关系信号台账（强制前置）**
参考 `prompts/relationship_signal_extractor.md` 和 `prompts/signal_weighting.md`：
- 先生成 `relationship_signal_ledger.jsonl` / `relationship_signal_ledger.md`
- 同步生成 `contradiction_ledger.md`
- T1 必须全量扫描：表白、拒绝、关系定义、条件性接受、边界、自我认知、未来时间线、矛盾/摇摆表达
- T4 只做统计和语言风格背景，不能推翻 T1
- 用户口述事件和用户纠正同等进入台账

**3b: Timeline First**
参考 `prompts/relationship_timeline_builder.md`：
- 用 T1/T2 划分关系阶段
- 每个阶段说明能判断什么、不能判断什么
- 避免用早期拒绝覆盖后期条件性表达，或用后期暧昧抹掉早期边界

**3c: 多因子解释**
参考 `prompts/multi_factor_interpreter.md`：
- 核心判断必须拆成多因子：感情/吸引、回避或自我保护、现实顾虑、愧疚、自我价值、安全/信任、用户压力
- 禁止把结论压成"喜欢/不喜欢"或"回避/不回避"二选一
- 如果 T1 不足，输出"不足以判断关系性质"

**3d: 当前局势判断**（优先于行动建议）
基于最近 1 个月的 T1/T2 信号：
- 当前关系阶段是什么
- 最近发生了什么关键事件
- 对方最近的态度/行为信号
- 趋势判断（升温/稳定/降温）
- 这是行动卡的直接输入
- 如果最近缺少 T1/T2，只能输出低置信度观察，不用 T4 补强

**3e: 沟通模式分析**
参考 `prompts/communication_analyzer.md`：
- 响应模式（响应时间、消息长度、开启话题）— 基于 T4 统计
- 情绪表达模式 — 基于 T2 信号
- 话题模式 — 基于 T3/T4
- 边界模式 — 基于 T2/T3
- 非字面表达模式 — 基于 T2/T3

**3f: 人格信号提取（6 层结构）**
参考 `prompts/persona_analyzer.md`：
- 基于关系信号台账中的 T1/T2 + 全时段 T3 信号
- 每条人格结论标注：稳定特征、压力状态、关系特定行为、自我陈述
- 依恋相关只输出"信号假设"，不输出诊断
- Layer 0：硬规则（"when X happens, then Y" 行为规则）
- Layer 1：身份定位（关系角色认知）
- Layer 2：表达风格（高频词、句式、表情、原话示例）
- Layer 3：决策模式（压力行为、说"不"方式）
- Layer 4：关系行为（亲近/疏远/冲突/修复）
- Layer 5：边界红线（显性/隐性边界）
- 每个维度必须有标签翻译 + 原话锚定

**3g: 依恋假设分析**
参考 `prompts/attachment_analyzer.md`：
- 基于 T2/T3 信号
- 纳入 T1 自我陈述，但必须同时检查行为反证
- 对方依恋信号（焦虑/回避/安全）
- 自我依恋信号
- 混合模式识别

**3h: 互动模式分析**
参考 `prompts/interaction_analyzer.md`：
- 基于全时段 T3 模式
- 正向循环
- 负向循环
- 冲突升级路径
- 修复信号

**3i: 生成报告**
参考 `prompts/report_builder.md`，生成报告：

- **Layer -1: 关系行动卡**（第一屏，仅引用通过审计的 T1/T2/T3 信号）
- Layer 0.5: 当前局势（最近 T1/T2 信号摘要）
- Layer 1.5: 关系信号台账摘要
- Layer 2-3: 双方人格画像（基于全时段 T2/T3 信号）
- Layer 4: 互动模式（基于 T3 模式）
- Layer 5: 依恋信号（基于 T2/T3）
- Layer 6: 沟通建议（基于人格画像 + 当前局势）
- Layer 7: 不确定性说明

**3j: 可靠性审计**
运行 `scripts/relationship_signal_audit.py`（或按其规则手动审计）：
- T1 是否全部进入主结论
- 是否存在 T4 覆盖 T1
- 是否遗漏用户纠正指出的证据
- 是否出现"就是不喜欢/就是回避型"等单因子断言
- 人格画像是否包含反证和替代解释

审计未通过时，报告状态必须是"低置信度草案"，行动卡只能输出补充语境和低风险观察。

每个主要结论必须使用固定格式：
- **观察**: 数据中看到了什么
- **证据**: E-YYYYMMDD-NNN（必须存在于 evidence_index.jsonl）
- **推断**: 从观察和证据中推断出什么
- **置信度**: 高/中/低
- **反证**: 支持相反结论的证据，或"无强反证"
- **替代解释**: 至少 1 个其他可能的解释
- **建议**: 基于此结论的行动建议（如适用）

报告开头必须包含覆盖声明（数据范围、总消息量、抽样说明）。

### Step 3j: 质量自检

生成报告后，执行以下自检：

1. **证据完整性**：每条核心结论是否都有证据 ID、置信度、替代解释
2. **风险词扫描**：检查是否使用了禁用词（肯定/一定/离不开/吃醋/PUA 等）
3. **覆盖声明**：大数据分析是否说明了抽样量和时间窗口
4. **Layer 完整性**：报告是否包含 Layer -1（行动卡）和 Layer 0-7
5. **关系信号审计**：T1 覆盖、T4 越权、单因子断言、人格画像反证是否通过

如发现违规，修正后再输出。

### Step 4: 教练对话

参考 `prompts/coach_mode.md`：

**开场**：总结 2-3 个发现，问用户想聊什么

```
我已经分析了你们的聊天记录。数据显示几个值得关注的模式：
1. {pattern_1}（证据：{IDs}）
2. {pattern_2}（证据：{IDs}）
3. {pattern_3}（证据：{IDs}）

你想先聊哪个方面？
```

**探索**：引用证据 → 置信度 → 替代解释 → 具体建议
**修正**：用户纠正 → 承认局限 → 更新理解
**指导**：用户问"我该怎么说" → 多语气草稿 + 推理
**收尾**：总结 → 未解决的问题 → 后续观察方向

### Step 5: 知识库管理

**首次分析**：生成知识库文件
- 对方画像（Layer 0-2 结构）
- 互动模式
- 依恋信号
- 不确定性说明

**后续更新**：参考 `prompts/merger.md`
- 增量合并，不覆盖已有结论
- 冲突检测，用户决定
- 版本管理，自动备份

## 进化模式

### 增量合并

当用户提供新数据时：
1. 分类新信息到对应维度
2. 检测与已有分析的冲突
3. 生成 Patch
4. 展示更新摘要
5. 用户确认后应用

参考 `prompts/merger.md`。

### 修正处理

当用户纠正分析时：
1. 理解纠正内容（场景、错误、正确）
2. 判断归属（哪个 Layer）
3. 生成 Correction 记录
4. 检查冲突
5. 确认并写入

参考 `prompts/correction_handler.md`。

## 输出要求

### 必须输出
1. **关系行动卡**（Layer -1，报告第一屏，1 分钟内回答"我现在该怎么做"）
2. 关系分析报告（Layer 0-7 完整结构）
3. 不确定性说明（每个结论的置信度、反证、替代解释）
4. 关系信号台账摘要与可靠性审计状态

### 可选输出（根据用户需求）
3. 沟通教练（多语气回复）
4. 消息草稿（温和版/直接版/降压版/有边界版）
5. 知识库文件或 Patch

### 语言规范

使用：
> 聊天记录呈现某些……信号。该判断置信度为……。替代解释包括……。

禁止：
> 对方就是……型。
> 对方一定……。
> 这能让对方离不开你。

## 框架文件引用

分析时参考以下框架：

- `references/frameworks/evidence_ladder.md` — 证据等级定义
- `references/frameworks/big_five_communication_signals.md` — 大五人格沟通信号
- `references/frameworks/attachment_anxiety_avoidance.md` — 依恋焦虑/回避信号
- `references/frameworks/relationship_communication_patterns.md` — 关系互动模式
- `references/frameworks/forbidden_overclaims.md` — 禁止的过度断言
- `references/frameworks/symbolic_mode_policy.md` — 星座/塔罗策略
- `references/frameworks/coaching_dialogue_framework.md` — 教练对话框架

## 禁止事项

### 绝对禁止
- 诊断人格类型或心理健康状态
- 提供操控、PUA、情感勒索建议
- 使用确定性语言（"他一定是..."、"他肯定..."）
- 预测关系结局
- 建议冷暴力、嫉妒诱导、消失测试

### 安全替代
| 禁忌表达 | 安全替代 |
|---------|---------|
| "他是回避型人格" | "聊天记录呈现一些回避相关信号" |
| "他一定不爱你" | "数据显示 {pattern}，但可能有其他解释" |
| "用冷落来测试他" | "建议直接沟通你的感受和需求" |
| "让他吃醋" | "建议通过正面方式表达你的价值" |

## 用户纠正的价值

用户纠正是系统最重要的学习信号之一：

1. **不要防御**：不要试图证明分析是对的
2. **优先用户判断**：用户比数据更了解对方
3. **询问细节**：用户的纠正可能包含重要上下文
4. **更新理解**：将纠正整合到知识库
5. **降低置信度**：如果用户纠正了关键观察，相关假设的置信度应降低
