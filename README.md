# LakeSkill 湖镜

> 把聊天记录放到一面安静的湖上。  
> 看见关系的倒影，也看见自己的心。

[English](README_EN.md) | [安装指南](INSTALL.md) | [快速开始](docs/quickstart.md) | [聊天记录准备](docs/chat_record_preparation.md)

[![CI](https://github.com/HZYO-0/lake-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/HZYO-0/lake-skill/actions/workflows/ci.yml)
[![Security](https://github.com/HZYO-0/lake-skill/actions/workflows/security.yml/badge.svg)](https://github.com/HZYO-0/lake-skill/actions/workflows/security.yml)

LakeSkill 湖镜是一个面向 Codex、Claude Code、OpenCode 等 agent runtime 的亲密关系聊天分析 Skill，并提供可选的本地预处理 CLI。

一句话定位：

> 别让 AI 猜 TA 爱不爱你。让 LakeSkill 告诉你：聊天证据支持什么、不支持什么、下一步怎么做更稳。

LakeSkill 不扮演 TA，不替你确认 TA 的真实内心，也不制造情绪依赖。它把聊天记录、关键事件和你的感受放回时间线，用证据 ID、置信度、反证和替代解释，先生成一张“湖镜行动卡”，再展开完整报告。

你会立刻得到：

- 一张行动卡：现在适合稳住、修复、轻推，还是先回到自己。
- 一组证据边界：哪些判断有证据，哪些只是情绪里的猜测。
- 一条更稳的下一步：本周做什么、不要做什么、可以怎么说。
- 一个隐私优先流程：本地脱敏、数据体检、打包，再考虑上传。

## 30 秒 Demo

输入可以很简单：

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

想做公开截图、长图或录屏脚本时，可以生成公开安全的合成示例：

```bash
lake-skill demo --out examples/social_demo
```

该命令还会生成 `examples/social_demo/social_assets/`，里面有长图文案、正文草稿、短视频录屏脚本和录屏检查清单。

## 先安装

### 方式 A：命令安装 Skill

```bash
npx skills add HZYO-0/lake-skill -y
```

查看仓库暴露的 Skill：

```bash
npx skills add HZYO-0/lake-skill --list
```

可安装 Skill 位于：

```text
skills/lake-skill/
```

Codex、Claude Code、OpenCode、手动安装和 ChatGPT Custom GPT 配置见 [INSTALL.md](INSTALL.md) 和 [docs/platform_compatibility.md](docs/platform_compatibility.md)。

### 方式 B：让 AI 助手帮你安装

如果你的 AI 助手能联网并操作本地终端，可以直接把这段发给它：

```text
请帮我在 GitHub 上找到 LakeSkill 湖镜，并安装到本地 agent runtime。
仓库地址：https://github.com/HZYO-0/lake-skill.git
安装后请确认 skills/lake-skill/SKILL.md 可用。
```

### 可选：安装本地预处理 CLI

数据量大或隐私敏感时，再安装 CLI：

```bash
git clone https://github.com/HZYO-0/lake-skill.git
cd lake-skill
pip install -e ".[dev]"
lake-skill version
```

如果你已经安装了依赖但命令找不到，先确认当前 Python 环境：

```bash
python -m lake_skill.cli version
```

Windows/PowerShell 如遇中文输出编码问题：

```powershell
$env:PYTHONUTF8="1"
$env:PYTHONIOENCODING="utf-8"
```

## 安装后怎么用

| 你是谁 | 最短用法 | 适合输出 |
|---|---|---|
| 非技术用户 | 安装 Skill 后，直接把一小段聊天粘给 agent | 局部观察、下一句话怎么说、低风险行动卡 |
| agent 用户 | 对 agent 说“使用 lake-skill，先给行动卡” | 行动卡、证据报告、消息草稿、沟通建议 |
| 隐私敏感用户 | 先用 CLI 本地脱敏、切分、体检，再上传产物 | 上传前数据体检、证据索引、完整报告 |

### 快速粘贴

```text
使用 lake-skill，帮我分析一下我们的聊天记录。先给行动卡。
```

适合一次具体互动、回复草稿、局部复盘。短样本不会支撑长期人格或关系模式判断。

### 隐私优先本地预处理

典型管线：

```bash
lake-skill ingest --file input/chat.csv --type csv --self-name 我 --target-name 对方 --out work/raw_messages.jsonl
lake-skill redact --file work/raw_messages.jsonl --out work/messages.redacted.jsonl --privacy-mode cloud-safe
lake-skill segment --file work/messages.redacted.jsonl --out work/sessions.redacted.jsonl
lake-skill digest --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --out work/digest.redacted.md
lake-skill evidence --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --out work/evidence.redacted.jsonl
lake-skill intake --out work --type ambiguous --status unknown --work-mode practical
lake-skill doctor --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --out work
lake-skill bundle --source work --out upload_bundle
```

`intake` 会生成 `lakeskill_intake.yaml` 和 `lakeskill_intake.md`，减少 agent 来回追问。`doctor` 会把数据可用性翻译成三档：只能局部观察 / 可出行动卡 / 可出完整报告。`bundle` 会把可上传产物整理到一个文件夹。

## 为什么可信

LakeSkill 的重点不是“更会猜”，而是让每个判断都有可检查的来源。

| 机制 | 作用 |
|---|---|
| Signal ledger first | 先生成关系信号台账，再写结论；避免凭整体感觉下判断 |
| T1-T4 weighting | 表白、拒绝、关系定义、边界和用户纠正优先；日常统计只能做背景 |
| Timeline first | 先分阶段，避免用早期拒绝覆盖后期变化，或用后期暧昧抹掉早期边界 |
| Multi-factor interpretation | 不把结论压成“喜欢/不喜欢”或“回避/不回避”二选一 |
| Reliability audit | 审计 T1 覆盖、T4 越权、单因子断言、反证和替代解释 |
| Confidence and counterevidence | 主要结论必须尽量说明置信度、反证和其他可能解释 |
| Privacy-first CLI | 大数据量或敏感数据可先在本地脱敏、切分、摘要和建证据索引 |

如果证据不足，LakeSkill 应明确降级：只输出低置信度局部观察，不生成完整人格或关系判断。

## 你会得到什么

### 湖镜行动卡

报告第一屏直接回答“我现在该怎么办”：

- 当前局势和最近趋势
- 当前策略：低压稳定 / 适度推进 / 冲突修复 / 暂时回到自己
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

LakeSkill 会基于证据、置信度和边界给出多种说法，而不是给操控策略。

## Use Cases

| 场景 | LakeSkill 可以做什么 |
|---|---|
| 暧昧推进 | 判断当前是否适合轻推、稳住或暂停，并给低压话术 |
| 关系修复 | 复盘冲突路径、修复信号和下一句怎么降低防御 |
| 冷淡复盘 | 区分短期忙碌、压力回避、边界信号和互动降温的证据 |
| 边界沟通 | 帮你表达需求而不施压、不审问、不把分析结果甩给对方 |
| 消息草稿 | 给温和版、直接版、降压版、有边界版等可发送句子 |
| 增量更新 | 合并新聊天记录和用户纠正，更新关系知识库 |

LakeSkill 不做：

- 医疗或心理健康判断
- 操控、嫉妒诱导、冷落测试
- 对他人意图的确定性断言
- 关系结局预测
- 前任、对象或同事的复活式模拟
- 数据库解密或绕过访问控制

## 为什么叫湖镜

湖有三层意思：

- **镜子**：像“潭面无风镜未磨”一样，关系证据先被照出来，而不是被情绪放大。
- **爱情**：西湖、断桥、诗歌和故事里，湖常常承载靠近、等待、错过和重逢。
- **安宁**：向外寻找答案之前，先向内找回自己的安稳。湖不是替你抓住谁，而是让你看清自己站在哪里。

所以 LakeSkill 不问“怎样控制一段关系”。它问的是：证据支持什么，不支持什么；现在适合靠近、稳定、修复，还是先回到自己。

## 版本与包

| 组件 | 版本 | 说明 |
|---|---:|---|
| Skill framework | 0.10.0 | `skills/lake-skill/SKILL.md` |
| Python CLI package | 0.10.0 | `lake-skill` 本地预处理工具 |
| Install path | `skills/lake-skill/` | GitHub 安装时使用的规范 Skill 包 |

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
