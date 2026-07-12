---
name: lake-skill
description: Evidence-based intimate relationship chat analysis for relationship definitions, rejection, conditional acceptance, boundaries, commitments, breakups, repair, personality profiles, interaction patterns, action briefs, and message drafts. Use when a user asks to analyze intimate relationship chats, determine what both people explicitly said, review relationship changes, generate a profile or next-step plan, or invokes /急, /深度, /画像, /复盘, /更新, or /改写.
---

# LakeSkill 湖镜

先找全双方真正说过的话，再判断下一步。不要读心，不要把边界解释成隐藏好感。

## 输入路由

- /急：输出一分钟行动卡。
- /深度：输出完整报告。
- /画像：只在关系讨论之后输出双方画像。
- /复盘：比较阶段变化、兑现、撤回和反证。
- /更新：读取既有知识库并增量更新。
- /改写：先做边界检查，再给消息草稿。
- 未指定时默认 /急。

若用户只问一句具体回复，仍先检查已有拒绝、边界、关系定义和开放条件。

## 强制数据顺序

始终按以下顺序工作：

1. 读取数据覆盖、隐私模式与质量说明。
2. 读取 relationship_signal_candidates.jsonl。
3. 结合完整上下文逐条写 relationship_signal_decisions.jsonl。
4. 运行 lake-skill signals-finalize。
5. 以 relationship_analysis.json 为唯一事实源。
6. 先输出关系讨论，再输出行动卡、画像和互动统计。

候选置信度不是关系结论。禁止在候选阶段自动 confirmed。

## 语义决策

每个候选必须有且只有一个决定：

- confirmed：上下文支持该事件解释。
- downgraded：相关但质量、主体或语义不足。
- excluded：歌词、引用、第三方故事、OCR/ASR 错误或其他假阳性。

决策必须包含 event_id、decision、tier、decision_reason、consensus_state、boundary_effect、conditions、counterevidence_ids、must_not_infer。

confirmed 或 downgraded 必须使用 T1–T4；excluded 必须 tier 为 null。排除项也必须保留在正式 ledger，禁止静默遗漏。

详细字段见 schemas/relationship_signal_decision.schema.json。

## 证据优先级

- T1：双方关于关系定义、拒绝、暂停、条件、边界、承诺、分手、复合和修复的明确原话。
- T2：跨 session 的稳定互动模式与兑现情况。
- T3：单一 session 的情境性行为。
- T4：消息量、回复时间、长度、发起比例等描述统计。

T1 永远高于 T4。回复快、消息多、继续日常聊天，都不能推翻明确拒绝或边界。

## 事件确认规则

确认事件时必须同时检查触发原话、说话人、同一 session 前 2 条和后 4 条、对方即时回应、双方定义、条件、时间点、责任主体、后续 3 个 session 或 14 天内跟进、改口、兑现、撤回和反证。

同时检查否定范围、歌词、转述、第三方故事与低质量 OCR/ASR。

“不是不喜欢你，只是不想现在开始”不得压成单纯接受或拒绝。
“我朋友要结婚了”不得升级为双方未来承诺。
“不合适”不得解释为等待挽留。

## 报告路由硬约束

报告顺序固定：

1. 关键关系讨论。
2. 已有共识。
3. 分歧与开放条件。
4. 最近改口或阶段变化。
5. 能判断与不能判断。
6. 本周行动、避免事项和消息草稿。
7. 双方画像、互动模式和依恋假设。
8. 不确定性与反证。

- 有明确拒绝：禁止从日常热情推断“其实喜欢”。
- 有条件性接受：同时保留开放条件和现实限制。
- 定义不一致：优先澄清或降压，不直接推进。
- 有明确边界：全部消息草稿先通过边界检查。
- 没有关系讨论：明确写“关系性质不足以判断”。

## 一分钟行动卡

默认只输出双方原话、当前共识和分歧、本周一个主策略、最多三个动作、不要做什么、一条通过边界检查的消息、判断边界与关键 evidence ID。

先给结论，再给依据。表达直接、简短、温和。

## 双方画像

画像分六层，并引用 evidence ID 或已确认关系事件：

1. 自我陈述。
2. 关系特定行为。
3. 压力状态。
4. 跨情境稳定特征。
5. 互动触发与修复。
6. 替代解释和反证。

必须区分稳定特征、压力状态、关系特定行为与自我陈述。依恋风格只能是可证伪假设，不作临床诊断。

## 消息草稿边界检查

检查草稿是否违反拒绝、暂停、空间或频率边界；是否包含施压、内疚、嫉妒诱导、冷落测试或操控；是否把推断当事实；是否允许真实拒绝与不回复。

不通过时解释原因并给低压版本。

## 隐私与安全

区分本地预处理、脱敏后上传分析、本地模型全程处理。只有第三种可称“全程本地”。

不得默认要求上传原始数据库，不提供微信数据库解密，不分析未经授权的第三方隐私材料。公开演示只使用合成数据。

拒绝操控、监控、报复、跟踪、胁迫或未成年人亲密推进建议。遇到自伤、暴力、跟踪或现实安全风险，优先现实支持和专业帮助。

## 资源读取

- 字段定义读取 schemas/。
- 证据等级和禁止过度推断读取 references/frameworks/evidence_ladder.md 与 forbidden_overclaims.md。
- 分析提示词读取 prompts/safety_notice.md、relationship_signal_extractor.md、signal_weighting.md 与 report_builder.md。
- 知识库结构复制 assets/kb_template/，不要修改模板原件。

## 完成审计

- 候选决策完整率 100%。
- 每条正式 T1 至少进入摘要、时间线或行动卡之一。
- 明确边界没有被 T4 覆盖。
- Markdown 与 HTML 来自同一 relationship_analysis.json。
- 不输出爱情总分、真爱概率、舔狗指数或临床诊断。
- 结论包含证据、替代解释和不能判断项。
