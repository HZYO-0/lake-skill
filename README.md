# BondLens 关系镜

> Not a partner simulator. An evidence-based relationship action card.<br>
> 不是把 TA 复活，而是帮你根据聊天证据少踩雷。

[English](README_EN.md) | [安装指南](INSTALL.md) | [快速开始](docs/quickstart.md) | [聊天记录准备](docs/chat_record_preparation.md)

[![CI](https://github.com/HZYO-0/bondlens/actions/workflows/ci.yml/badge.svg)](https://github.com/HZYO-0/bondlens/actions/workflows/ci.yml)
[![Security](https://github.com/HZYO-0/bondlens/actions/workflows/security.yml/badge.svg)](https://github.com/HZYO-0/bondlens/actions/workflows/security.yml)

BondLens 是一个面向 Codex、Claude Code、OpenCode 等 agent runtime 的亲密关系聊天分析 Skill，并提供可选的本地预处理 CLI。它不模拟前任、对象或某个具体的人，而是把聊天记录转成可审计的关系行动卡：现在是什么局势，本周怎么做，哪些判断不能过度解读，下一句话可以怎么发。

当前版本：

| 组件 | 版本 | 说明 |
|---|---:|---|
| Skill framework | 0.9.0 | `skills/bondlens/SKILL.md` |
| Python CLI package | 0.9.0 | `bondlens` 本地预处理工具 |
| Install path | `skills/bondlens/` | GitHub 安装时使用的规范 Skill 包 |

---

## 30 秒 Demo

输入可以很简单：

```text
使用 bondlens，帮我分析这段聊天记录。我的目标是知道下一步怎么做。

[2026-06-01 22:13] 我: 最近感觉你有点少回我，我是不是哪里做错了？
[2026-06-01 22:18] TA: 没有，就是这几天事情比较多。
[2026-06-02 09:10] TA: 昨天那个资料你还有吗？
```

BondLens 的第一屏不是长篇人格分析，而是行动卡：

```markdown
## 先看这个：关系行动卡

### 当前策略
低压稳定。

为什么是这个策略：
对方在情绪确认问题上没有展开，但也没有切断日常互动；第二天仍主动发起求助。
证据：E-20260601-001, E-20260602-001
置信度：低到中。样本太短，只能判断这个局部场景。

### 本周 3 个动作
1. 先恢复日常节奏，不连续追问“是不是我错了”。
2. 对方求助时正常回应，帮完不追加情绪索取。
3. 如果要表达感受，用一句低压说明，不要求对方立刻表态。

### 不要做
- 不要用“你为什么不回应我”开场。
- 不要把一次短回复直接解释成“不在乎”。
- 不要用分析结果教育对方。

### 可直接发送
“这两天我有点敏感，刚刚那句不是想给你压力。资料我发你，忙完再说就好。”
```

---

## BondLens 和 ex-skill / colleague-skill 有什么不同

Skill 社区里有很多优秀项目在做 person distillation 或 persona simulation，例如把前任、同事、角色或某类人“蒸馏”为可对话对象。BondLens 走的是另一条线：不扮演 TA，而是解释证据。

| 类型 | 典型目标 | 典型输出 | BondLens 的区别 |
|---|---|---|---|
| dot-skill / colleague-style | 把某个人、同事或角色知识打包成 Skill | 像某个人一样反馈、吐槽、复盘或陪聊 | BondLens 不模拟某个人的声音，只分析聊天证据支持什么 |
| ex-skill-style | 把前任或过去关系蒸馏成可交互 persona | 情绪化回看、对话模拟、记忆式互动 | BondLens 不复活关系对象，不预测 TA 的真实内心 |
| BondLens | 把聊天记录变成行动判断 | 行动卡、证据报告、消息草稿、审计说明 | 核心是 evidence interpretation + action coaching |

一句话定位：别让 AI 猜 TA 爱不爱你。让 BondLens 告诉你：聊天证据支持什么、不支持什么、下一步怎么做更安全。

---

## 你会得到什么

### 关系行动卡

报告第一屏直接回答“我现在该怎么办”：

- 当前局势和最近趋势
- 当前策略：低压稳定 / 适度推进 / 冲突修复
- 本周 3 个具体动作
- 不要做的事
- 此前踩雷点复盘
- 往后要观察的信号
- 可直接发送的话术

### 证据报告

完整报告解释行动卡为什么这样判断：

- 关系时间线和关键事件
- 关系信号台账摘要
- 双方沟通画像与原话锚定
- 互动循环、冲突路径、修复信号
- 非临床依恋信号假设
- 每个核心判断尽量给出置信度、反证和替代解释

### 教练模式

你可以继续追问：

```text
我该怎么说？
TA 这句话什么意思？
我是不是踩雷了？
下一步该推进还是稳住？
这句话会不会太压迫？
```

BondLens 会基于证据、置信度和边界给出多种说法，而不是给操控策略。

---

## Why Trust It

BondLens 的重点不是“更会猜”，而是让每个判断都有可检查的来源。

| 机制 | 作用 |
|---|---|
| Signal ledger first | 先生成关系信号台账，再写结论；避免凭整体感觉下判断 |
| T1-T4 weighting | 表白、拒绝、关系定义、边界和用户纠正优先；日常统计只能做背景 |
| Timeline first | 先分阶段，避免用早期拒绝覆盖后期变化，或用后期暧昧抹掉早期边界 |
| Multi-factor interpretation | 不把结论压成“喜欢/不喜欢”或“回避/不回避”二选一 |
| Reliability audit | 审计 T1 覆盖、T4 越权、单因子断言、反证和替代解释 |
| Confidence and counterevidence | 主要结论必须尽量说明置信度、反证和其他可能解释 |
| Privacy-first CLI | 大数据量或敏感数据可先在本地脱敏、切分、摘要和建证据索引 |

如果证据不足，BondLens 应该明确降级：只输出低置信度局部观察，不生成完整人格或关系判断。

---

## Use Cases

| 场景 | BondLens 可以做什么 |
|---|---|
| 暧昧推进 | 判断当前是否适合轻推、稳住或暂停，并给低压话术 |
| 关系修复 | 复盘冲突路径、修复信号和下一句怎么降低防御 |
| 冷淡复盘 | 区分短期忙碌、压力回避、边界信号和互动降温的证据 |
| 边界沟通 | 帮你表达需求而不施压、不审问、不把分析结果甩给对方 |
| 消息草稿 | 给温和版、直接版、降压版、有边界版等可发送句子 |
| 增量更新 | 合并新聊天记录和用户纠正，更新关系知识库 |

BondLens 不做：

- 临床诊断
- PUA、操控、嫉妒诱导、冷落测试
- 对他人意图的确定性断言
- 关系结局预测
- 前任、对象或同事的复活式模拟
- 数据库解密或绕过访问控制

---

## 安装

安装 Skill：

```bash
npx skills add HZYO-0/bondlens -y
```

查看仓库暴露的 Skill：

```bash
npx skills add HZYO-0/bondlens --list
```

可安装 Skill 位于：

```text
skills/bondlens/
```

Codex、Claude Code、OpenCode、手动安装和 ChatGPT Custom GPT 配置见 [INSTALL.md](INSTALL.md) 和 [docs/platform_compatibility.md](docs/platform_compatibility.md)。

---

## 快速开始

安装后，新开一个 agent 会话：

```text
使用 bondlens，帮我分析一下我们的聊天记录
```

然后提供以下任一种输入：

- 直接粘贴聊天片段
- 上传 TXT/CSV/JSONL 聊天文件
- 上传本地预处理产物：`digest`、`sessions`、`evidence`，以及可选知识库文件

如果数据量大或隐私敏感，可以用 CLI 做本地预处理：

```bash
git clone https://github.com/HZYO-0/bondlens.git
cd bondlens
pip install -e ".[dev]"
bondlens init ./my_project
```

典型本地管线：

```bash
bondlens ingest --file input/chat.csv --type csv --self-name 我 --target-name 对方 --out work/raw_messages.jsonl
bondlens redact --file work/raw_messages.jsonl --out work/messages.redacted.jsonl --privacy-mode cloud-safe
bondlens segment --file work/messages.redacted.jsonl --out work/sessions.redacted.jsonl
bondlens digest --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --out work/digest.redacted.md
bondlens evidence --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --out work/evidence.redacted.jsonl
```

更多步骤见 [docs/quickstart.md](docs/quickstart.md) 和 [docs/chat_record_preparation.md](docs/chat_record_preparation.md)。

---

## 第一次分析需要多少聊天记录

少量片段也能分析，但稳定的关系判断需要足够上下文。

| 数据量 | 适合做什么 | 预期置信度 |
|---|---|---|
| 5-30 条 | 看一个局部场景，起草一句回复 | 低 |
| 30-100 条 | 初步识别沟通信号 | 低到中 |
| 跨数天 100+ 条 | 行动卡 + 聚焦报告 | 中 |
| 数周到数月，场景多样 | 完整报告 + 手册 + 知识库 | 中到高 |

推荐覆盖这些场景：

- 日常聊天
- 求助或帮忙
- 冲突或压力
- 修复或道歉
- 冷淡或延迟回复
- 升温或亲密时刻
- 边界讨论

---

## 工作流

1. **Intake**：关系类型、当前状态、双方称呼、分析目标、数据来源。
2. **Data check**：消息量、时间跨度、双方参与度、场景多样性。
3. **Local preprocessing**：可选脱敏、会话切分、摘要、证据索引。
4. **Signal ledger**：先提取 T1-T4 关系信号和矛盾台账。
5. **Action card**：先给用户下一步怎么做。
6. **Full report**：Layer -1 到 Layer 7 的证据报告。
7. **Audit**：证据完整性、风险词、覆盖声明、不确定性检查。
8. **Update**：合并新数据和用户纠正，更新知识库。

---

## 报告结构

| 层级 | 作用 |
|---|---|
| Layer -1 | 关系行动卡 |
| Layer 0 | 核心行为规则 |
| Layer 0.5 | 当前局势 |
| Layer 1 | 关系背景和时间线 |
| Layer 1.5 | 关系信号台账摘要 |
| Layer 2 | 对方画像，原话锚定 |
| Layer 3 | 自我画像，原话锚定 |
| Layer 4 | 互动模式 |
| Layer 5 | 非临床依恋信号 |
| Layer 6 | 沟通手册和消息草稿 |
| Layer 7 | 不确定性、反证、替代解释 |

---

## 项目结构

```text
skills/bondlens/           可安装的 Skill 包
  SKILL.md                 Skill 指令
  prompts/                 分析和教练 prompt 模块
  references/frameworks/   证据、依恋、沟通、安全框架
  assets/kb_template/      增量知识库模板
cli/bondlens/              可选本地预处理 CLI
docs/                      用户、平台兼容和宣传文档
examples/                  合成示例输入和期望输出结构
tests/                     CLI、解析器、安全和审计测试
```

---

## License

MIT License. See [LICENSE](LICENSE).
