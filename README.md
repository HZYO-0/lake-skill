# BondLens 关系镜

> 把聊天记录变成一张可执行的关系行动卡：现在什么局势、本周怎么做、哪些雷别踩、下一句可以怎么发。

[![CI](https://github.com/HZYO-0/bondlens/actions/workflows/ci.yml/badge.svg)](https://github.com/HZYO-0/bondlens/actions/workflows/ci.yml)
[![Security](https://github.com/HZYO-0/bondlens/actions/workflows/security.yml/badge.svg)](https://github.com/HZYO-0/bondlens/actions/workflows/security.yml)

BondLens 是一个基于证据的亲密关系聊天分析 Skill，并提供可选的本地预处理 CLI。它不是为了给你一份很长的心理分析报告，而是先回答最实际的问题：聊天记录说明了什么，哪些地方不确定，你现在该怎么做才不越界、不施压、不自我内耗。

---

## 你会得到什么

BondLens v4.1 把最有用的部分放在最前面。

### 1. 关系行动卡

报告第一屏直接回答：“我现在该怎么办？”

- 当前局势
- 当前策略：低压稳定 / 适度推进 / 冲突修复
- 本周 3 个具体动作
- 不要做的事
- 此前踩雷点复盘
- 往后要观察的信号
- 可以直接发送的话术

### 2. 证据报告

完整报告解释行动卡为什么这样判断。

- 用行为规则替代人格标签
- 双方人格画像都有原话锚定
- 互动循环、冲突路径、修复信号
- 非临床依恋信号假设
- 每个核心判断尽量给出置信度、反证和替代解释

### 3. 教练模式

你可以继续追问：

```text
我该怎么说？
她这句话什么意思？
我是不是踩雷了？
下一步该推进还是稳住？
```

BondLens 会基于证据、置信度和边界给出具体说法。

---

## 效果预览

不是这样：

```text
建议保持适度联系，给对方一些空间。
```

而是这样：

```markdown
## 先看这个：关系行动卡

### 当前策略
低压稳定

为什么是这个策略：
对方在情感话题后回复变短，并用时间点结束对话（E-20260604-001, E-20260604-002）。
但日常求助和轻松聊天仍然顺畅（E-20260603-004, E-20260605-001）。

### 本周 3 个动作
1. 保持日常节奏，不突然加大关心频率。
2. 她主动求助时正常帮忙，帮完不要邀功。
3. 情感话题如果被她接住就轻轻说；如果她变短，立刻转回轻松话题。

### 不要做
- 不要问“你为什么不回应我”。
- 不要用分析结果教育她。
- 不要把帮忙变成情感交换。
```

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

如果数据太薄，BondLens 应该明确说明，只给低置信度的局部观察。

---

## 安装

安装 Skill：

```bash
npx skills add HZYO-0/bondlens -y
```

可安装的 Skill 位于：

```text
skills/bondlens/
```

Codex、Claude Code、手动安装和 ChatGPT Custom GPT 配置见 [INSTALL.md](INSTALL.md)。

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

更多步骤见 [docs/quickstart.md](docs/quickstart.md) 和 [docs/chat_record_preparation.md](docs/chat_record_preparation.md)。

---

## 工作流

BondLens 借鉴 PaperSpine 的工作流思想：先做 intake 和配置，再分析，最后用 audit 校验输出可信度。

1. **Intake**：关系类型、当前状态、双方称呼、分析目标、数据来源。
2. **Data check**：消息量、时间跨度、双方参与度、场景多样性。
3. **Local preprocessing**：可选脱敏、会话切分、摘要、证据索引。
4. **Action card**：先给用户下一步怎么做。
5. **Full report**：Layer 0-7 证据报告。
6. **Audit**：证据完整性、风险词、覆盖声明、不确定性检查。
7. **Update**：合并新数据和用户纠正，更新知识库。

---

## 报告结构

| 层级 | 作用 |
|---|---|
| Layer -1 | 关系行动卡 |
| Layer 0 | 核心行为规则 |
| Layer 1 | 关系背景和时间线 |
| Layer 2 | 对方画像，原话锚定 |
| Layer 3 | 自我画像，原话锚定 |
| Layer 4 | 互动模式 |
| Layer 5 | 非临床依恋信号 |
| Layer 6 | 沟通手册和消息草稿 |
| Layer 7 | 不确定性、反证、替代解释 |

---

## 安全边界

BondLens 不提供：

- 临床诊断
- PUA、操控、嫉妒诱导、冷落测试
- 对他人意图的确定性断言
- 关系结局预测
- 数据库解密或绕过访问控制

必须使用更安全的表达：聊天记录呈现某些信号、置信度为中、替代解释包括……

---

## 项目结构

```text
skills/bondlens/           可安装的 Skill 包
  SKILL.md                 Skill 指令
  prompts/                 分析和教练 prompt 模块
  references/frameworks/   证据、依恋、沟通、安全框架
  assets/kb_template/      增量知识库模板
cli/bondlens/              可选本地预处理 CLI
docs/                      用户和开发文档
analyses/                  示例分析产物
tests/                     CLI 和解析器测试
```

---

## License

MIT License. See [LICENSE](LICENSE).
