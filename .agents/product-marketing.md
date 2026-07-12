# Product Marketing Context

*Last updated: 2026-07-12*

## Product Overview
**One-liner:** 别让 AI 猜 TA 爱不爱你。先把双方真正说过的话找全，再判断下一步怎么做。
**Category:** 隐私优先、证据型关系聊天分析工具。
**Product type:** MIT 开源核心、本地 CLI、多平台 AI Skill。
**Business model:** 核心免费；可选本地部署、数据整理、私有分析流程和定制报告模板；不做情感陪伴 SaaS。

## Target Audience
**Primary:** 对关系讨论困惑、需要可执行建议，但不希望被 AI 煽动或读心的人。
**Secondary:** Codex/Claude Skill 用户、聊天数据分析开发者。
**Anti-persona:** 寻求操控、读心、临床诊断、监控第三方、报复或未成年人亲密推进建议的人。

## Jobs to Be Done
- 找全双方真正谈过的关系定义、条件和边界。
- 区分事实、推断与不能判断。
- 得到不越界的行动卡与消息草稿。
- 在交给模型前本地整理、脱敏和审计聊天数据。

## Problems
常见恋爱分析把回复速度、消息比例或少量抽样放大为“喜欢/不喜欢”，却漏掉明确讨论过的关系问题。候选常被直接当结论，单一分数制造虚假精确度，拒绝和边界甚至被解释成隐藏好感。

## Competitive Landscape
**Direct:** she-love-me 与其他恋爱分析 Skills。导入、统计和 HTML 展示往往更成熟，但证据分层、候选/结论分离和边界优先不稳定。
**Secondary:** 通用 LLM 直接分析聊天。上手快，但容易抽样、遗漏、读心。
**Indirect:** 人工复盘、朋友建议和情感咨询。

## Differentiation
- 关系讨论全量扫描先于采样。
- 候选、Skill 决策和正式台账三段分离。
- 明确拒绝、边界与关系定义永远高于 T4 热度。
- 每条正式事件有证据、上下文、反证和禁止推断。
- Markdown 与无外链 HTML 来自同一 JSON。
- 公开 Demo 只用合成数据，不宣传爱情判断准确率。

## Objections
| Objection | Response |
|---|---|
| AI 还是会猜错 | 候选不是结论；必须逐条确认、降级或排除。 |
| 聊天记录太隐私 | 支持本地预处理、脱敏后上传和本地模型三种边界。 |
| 为什么没有爱情总分 | 总分会掩盖定义、条件与边界。 |
| 对方每天聊天是不是仍然喜欢 | 日常互动只是 T4，不能覆盖明确拒绝。 |

## Customer Language
- “我们明明谈过关系，为什么 AI 只分析回复速度？”
- “不是不喜欢，只是现在不能开始，到底算什么？”
- “拒绝后还每天聊天，AI 为什么总说其实喜欢？”
- “我不想把原始聊天数据库上传。”

**Words to use:** 原话、关系讨论、边界、开放条件、反证、可核查、不知道、低压。
**Words to avoid:** 真爱概率、被爱指数、舔狗指数、拿捏、让 TA 上头、保证复合。

## Brand Voice
冷静、直接、温和、可核查、不站队。先结论后依据；承认不知道；不刺激焦虑；不攻击竞品。

## Proof Points
| Theme | Proof |
|---|---|
| 决策完整 | finalize 要求每个候选恰好一个决定 |
| T1 不遗漏 | 关系讨论全量保留且优先于采样 |
| 边界优先 | 明确拒绝禁止被日常互动重解释 |
| 可审计 | 候选、决策、台账、JSON 与报告均可检查 |
| 隐私可信 | 无外链 HTML、无默认遥测、公开素材全合成 |

## Goals
**Conversion action:** GitHub 搜索 LakeSkill 湖镜，先运行合成 Demo，再决定是否导入自己的记录。
**Success metrics:** 5 分钟 Demo、process/报告成功率、候选决策完整率、T1 覆盖率、GitHub/PyPI 与公开内容趋势。
**Never use:** 复合率、真爱准确率、让 TA 主动率。
