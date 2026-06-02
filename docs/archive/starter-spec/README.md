# WeChat Relationship Insight 项目构建包

这是一个用于启动 `wechat-relationship-insight` 项目的构建方案与开发说明包。它不是最终实现，而是给 AI coding agent / 开发者使用的项目蓝图。

## 默认产品模式

默认采用：

```text
本地预处理 + ChatGPT Skill 分析
```

也就是：原始微信数据库、原始语音、原始截图和完整聊天全文尽量只在本地处理；本地生成脱敏后的摘要、会话切片和证据索引；再把 `digest.redacted.md`、`evidence_index.redacted.jsonl`、`session_summaries.redacted.jsonl`、旧知识库等上传给 ChatGPT Skill 做亲密关系画像、依恋/人格信号分析、互动模式分析、后续沟通建议和知识库更新。

## 你应该先读哪些文件

建议按顺序阅读：

1. `AI_DEVELOPMENT_BRIEF.md`：给 AI coding agent 的总指令。
2. `PROJECT_SPEC.md`：完整产品与边界定义。
3. `ARCHITECTURE.md`：仓库结构、数据流、组件设计。
4. `TECHNICAL_DETAILS.md`：技术细节、数据 schema、CLI、隐私模式。
5. `ANALYSIS_FRAMEWORK.md`：人格、依恋、证据等级、星座/塔罗策略。
6. `DEVELOPMENT_PLAN.md`：阶段开发计划和验收标准。
7. `TEST_PLAN.md`：测试方案、测试节点、安全评测。
8. `DEPLOYMENT_PLAN.md`：本地、混合、Skill、Docker、CI/CD 发布方案。
9. `PRIVACY_SECURITY.md`：隐私、安全、威胁模型和开源注意事项。

## 本包内容

```text
.
├── README.md
├── AI_DEVELOPMENT_BRIEF.md
├── PROJECT_SPEC.md
├── ARCHITECTURE.md
├── TECHNICAL_DETAILS.md
├── ANALYSIS_FRAMEWORK.md
├── DEVELOPMENT_PLAN.md
├── TEST_PLAN.md
├── DEPLOYMENT_PLAN.md
├── PRIVACY_SECURITY.md
├── BACKLOG.md
├── config.default.yaml
├── .gitignore.template
├── pyproject.toml.template
├── skill/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── references/frameworks/*.md
│   └── assets/kb_template/*.md
└── docs/
    ├── source_references.md
    └── release_checklist.md
```

## 开发原则

- 不做微信数据库解密或越权读取。
- 默认只上传本地脱敏摘要和证据索引给 ChatGPT Skill。
- 不做临床诊断，不断言“对方就是某人格/某依恋类型”。
- 不提供操控、PUA、骚扰、诱导嫉妒、冷暴力测试等话术。
- 人格/依恋分析必须基于聊天证据、重复模式、置信度、反证和替代解释。
- 星座、塔罗、占卜不进入核心证据模型；如保留，只能作为默认关闭的娱乐性“象征反思模式”。
