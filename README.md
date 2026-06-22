# LakeSkill 湖镜

> *"我之前一直问 AI 'TA 到底喜不喜欢我'，它每次都给一个很肯定的答案，但我越看越焦虑。用了 LakeSkill 才发现，原来它应该先告诉我'证据不够'。"*

**别让 AI 猜 TA 爱不爱你。让聊天证据自己说话。**

[English](README_EN.md) | [安装指南](INSTALL.md) | [快速开始](docs/quickstart.md) | [聊天记录准备](docs/chat_record_preparation.md)

[![CI](https://github.com/HZYO-0/lake-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/HZYO-0/lake-skill/actions/workflows/ci.yml)
[![Security](https://github.com/HZYO-0/lake-skill/actions/workflows/security.yml/badge.svg)](https://github.com/HZYO-0/lake-skill/actions/workflows/security.yml)

粘贴一段聊天记录，LakeSkill 会：

- 告诉你**证据支持什么**，不支持什么——不靠猜
- 给你一张**行动卡**：本周该做什么、不要做什么、可以怎么说
- 每条判断标上**证据 ID 和置信度**，如果证据不够会降级，不硬撑结论

> ⚠️ LakeSkill 不扮演 TA，不替你确认 TA 的真实内心，不制造情绪依赖，不提供操控策略。

## 先看效果

### 场景一：粘贴一段聊天

输入：

```text
使用 lake-skill，帮我分析这段聊天记录。我的目标是知道下一步怎么做。

[2026-06-01 22:13] 我: 最近感觉你有点少回我，我是不是哪里做错了？
[2026-06-01 22:18] TA: 没有，就是这几天事情比较多。
[2026-06-02 09:10] TA: 昨天那个资料你还有吗？
```

LakeSkill 的第一屏不是长篇人格分析，而是湖镜行动卡：

```markdown
## 先看这个：湖镜行动卡（关系行动卡）

### 当前策略
低压稳定。

为什么是这个策略：
对方在情绪确认问题上没有展开，但也没有切断日常互动；第二天仍主动发起求助。
证据：E-20260601-001, E-20260602-001
置信度：低到中。样本太短，只能判断这个局部场景。

### 本周 3 个动作
1. 先恢复日常节奏，不连续追问"是不是我错了"。
2. 对方求助时正常回应，帮完不追加情绪索取。
3. 如果要表达感受，用一句低压说明，不要求对方立刻表态。

### 不要做
- 不要用"你为什么不回应我"开场。
- 不要把一次短回复直接解释成"不在乎"。
- 不要用分析结果教育对方。

### 可直接发送
"这两天我有点敏感，刚刚那句不是想给你压力。资料我发你，忙完再说就好。"
```

### 场景二：继续追问

```text
用户: TA 这句话什么意思？
```

```markdown
这句话的字面意思是求助，但结合前一条"事情比较多"，它可能是在用实际需求确认你是否还在。
证据：E-20260602-001
置信度：低。替代解释：可能只是真的需要资料，没有更深含义。
```

### 场景三：证据不够时

```text
用户: TA 到底喜不喜欢我？
```

```markdown
当前数据不足以判断关系性质。你提供的 3 条消息中没有表白、拒绝或关系定义信号。
建议补充：更多日常互动、冲突场景、对方主动发起的对话。
```

想截图发小红书、抖音录屏或做教程？一键生成公开安全的合成素材：

```bash
lake-skill demo --out examples/social_demo
```

## 安装

```bash
npx skills add HZYO-0/lake-skill -y
```

或让 AI 助手帮你装：

```text
请帮我在 GitHub 上找到 LakeSkill 湖镜，并安装到本地。
仓库地址：https://github.com/HZYO-0/lake-skill.git
```

从微信导出聊天记录？用 [WeChatDataAnalysis](https://github.com/LifeArchiveProject/WeChatDataAnalysis) 解密后导入。教程见 [docs/wechat_data_analysis_guide.md](docs/wechat_data_analysis_guide.md)。

更多安装方式（Codex、Claude Code、手动、ChatGPT GPT）见 [INSTALL.md](INSTALL.md)。

## 怎么用

| 你是谁 | 最短路径 | 你会得到 |
|---|---|---|
| 非技术用户 | 安装后直接粘一小段聊天 | 局部观察、下一句话怎么说、行动卡 |
| agent 用户 | 说"使用 lake-skill，先给行动卡" | 行动卡、证据报告、消息草稿 |
| 隐私敏感用户 | CLI 本地脱敏后再上传 | 数据体检、证据索引、完整报告 |

不确定？先装好，粘一段聊天试一次。5 分钟就知道适不适合。

```text
使用 lake-skill，帮我分析一下我们的聊天记录。先给行动卡。
```

## 适合什么场景

暧昧推进、关系修复、冷淡复盘、边界沟通、消息草稿、增量更新——都用同一套证据框架。

不做：医疗诊断、操控策略、关系预测、数据库解密。

## 为什么可信

1. **先看证据，再下结论**：每条判断必须有证据 ID，没有就是猜。
2. **不确定就降级**：证据不够时只给低风险观察，不硬撑完整判断。
3. **每条结论有反证**：不只给你一个答案，还告诉你什么情况下可能是错的。

如果证据不足，LakeSkill 会明确说"当前数据不足以判断"，而不是用模糊措辞掩盖。

## 为什么叫湖镜

湖像镜子。关系证据先被照出来，而不是被情绪放大。

西湖、断桥、诗歌里，湖承载靠近、等待、错过和重逢。

向外找答案之前，先向内找回自己的安稳。

## 项目结构

```text
skills/lake-skill/        可安装的 Skill 包
  SKILL.md                Skill 指令
  prompts/                分析和教练 prompt 模块
  references/frameworks/  证据、依恋、沟通、安全框架
  assets/kb_template/     增量知识库模板
cli/lake_skill/           可选本地预处理 CLI
docs/                     用户、安装和平台兼容文档
examples/                 合成示例输入和期望输出结构
tests/                    CLI、解析器、安全和审计测试
```

## License

MIT License. See [LICENSE](LICENSE).
