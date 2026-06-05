# BondLens 关系镜

> 翻聊天记录翻到凌晨三点，不是因为你想回忆过去，是因为你想搞清楚——TA 到底什么意思，你现在该怎么办。

[![CI](https://github.com/HZYO-0/bondlens/actions/workflows/ci.yml/badge.svg)](https://github.com/HZYO-0/bondlens/actions/workflows/ci.yml)
[![Security](https://github.com/HZYO-0/bondlens/actions/workflows/security.yml/badge.svg)](https://github.com/HZYO-0/bondlens/actions/workflows/security.yml)

---

## 这是什么

把你和某个人的聊天记录丢给 BondLens，它会告诉你三件事：

1. **TA 是什么样的人** —— 不是"回避型依恋"这种标签，而是"当你连续关心超过 3 条，TA 会说'不用讷'来设立距离"这种具体规则
2. **你们之间是什么模式** —— 谁在主动、谁在回避、冲突怎么升级、什么信号说明 TA 在修复
3. **你现在该怎么做** —— 不是"建议你保持适度联系"，而是"明天别主动找她，后天发个食堂吐槽破冰，因为 TA 的模式是..."

它不会告诉你"TA 一定喜欢你"。它会说："数据显示某些积极信号，置信度中等，反证包括...，但 TA 的回避模式在压力下会被激活。"

---

## 效果预览

丢进去 200 条聊天记录，你会得到这样的东西：

**人格画像不是标签，是行为规则：**

```markdown
Layer 0 硬规则

规则 1：当被问"我们什么关系"时，Tf 会用转移话题或沉默回应
  原话：[2026-05-28] Tf: 保持低调感别说话
  置信度：中

规则 2：当 Zy 连续关心超过 3 条时，Tf 会说"不用"来设立距离
  原话：[2026-04-19] Tf: 不用讷，你太辛苦了，熬大夜，赶紧吃完回去睡觉
```

**建议不是废话，是场景剧本：**

```markdown
场景：答辩后疏离期

触发条件：Tf 回复变慢（>2 小时），消息变短（≤3 字符）
她的可能心理：答辩完累了 + 上次表白的事还在消化

推荐做法：
1. 前两天别主动找她
2. 第三天发个食堂吐槽："今天那个红烧肉，我怀疑是用橡皮做的"
   为什么：用你们平时的方式破冰，不涉及关系
3. 她回应了就正常聊，没回应就再等一天

禁止：
- "你怎么不理我"
- "是不是我上次说错话了"
```

---

## 安装

```text
帮我安装这个 skill：https://github.com/HZYO-0/bondlens/tree/main/skills/bondlens
```

或：

```bash
npx skills add HZYO-0/bondlens -y
```

支持：Claude Code、Codex、OpenCode、OpenClaw 等运行时。

ChatGPT 用户：创建 GPT → 粘贴 [`SKILL.md`](skills/bondlens/SKILL.md) 到 Instructions → 上传 [`references/frameworks/`](skills/bondlens/references/frameworks/) 里的 7 个文件到 Knowledge。

详细安装说明见 [`INSTALL.md`](INSTALL.md)。

---

## 使用

安装后直接说：

```text
帮我分析一下我们的聊天记录
```

然后粘贴或上传聊天记录。

| 输入量 | 你能得到 |
|--------|---------|
| 5-10 条 | 低置信度的局部观察 |
| 30+ 条 | 初步校准分析 |
| 100+ 条，场景多样 | 完整人格画像 + 互动模式 + 场景剧本 |

---

## 分析产出

8 层结构报告：

| 层级 | 回答什么问题 |
|------|-------------|
| Layer 0 | TA 的行为规则是什么？（when X then Y） |
| Layer 1 | 你们的关系背景和时间线 |
| Layer 2 | TA 是什么样的人？（6 层人格画像 + 原话锚定） |
| Layer 3 | 我是什么样的人？ |
| Layer 4 | 我们之间的互动模式？（正向循环、负向循环、冲突路径） |
| Layer 5 | 依恋信号？（焦虑/回避/安全） |
| Layer 6 | 我现在该怎么做？（场景剧本 + 消息草稿） |
| Layer 7 | 哪些结论不确定？（置信度、反证、替代解释） |

---

## 工作模式

| 模式 | 适用场景 | 输出风格 |
|------|---------|---------|
| `support` | 你心情不好，想有人听你说 | 先共情，再给建议 |
| `practical` | 你想知道下一步怎么做 | 先判断局势，再给动作 |
| `repair` | 你们吵架了/冷战了 | 先分析冲突，再给修复步骤 |
| `auto` | 默认 | 根据你说的话自动判断 |

---

## 支持的数据格式

| 来源 | 格式 |
|------|------|
| 微信桌面版导出 | TXT, CSV |
| 通用表格 | CSV, TSV |
| 结构化消息 | JSONL |
| 纯文本数据库 | SQLite（不解密） |
| 语音转写 | SRT, VTT |
| OCR 转写 | CSV, JSONL |

---

## 安全边界

BondLens 拒绝：临床诊断、操控/PUA/情感勒索、关于他人意图的确定性断言、关系结局预测、解密受保护的聊天数据库。

---

## 项目结构

```
├── skills/bondlens/           # 可安装的 Skill 包
│   ├── SKILL.md               # Skill 指令（v4）
│   ├── prompts/               # 分析 prompt 模板
│   ├── references/frameworks/ # 参考框架
│   └── assets/kb_template/    # 知识库模板
├── cli/bondlens/              # Python CLI（本地预处理）
├── docs/                      # 文档
├── examples/                  # 示例
└── tests/                     # 测试
```

---

## 写在最后

前任.skill 帮你把过去的回忆存起来，然后教你放下。

BondLens 帮你把现在的聊天记录看清楚，然后教你下一步怎么走。

一个向后看，一个向前看。

你凌晨三点翻聊天记录，不是为了怀旧。你想知道的是：TA 到底什么意思，我现在该怎么办。

BondLens 就是回答这个问题的。

---

## License

MIT License. See [`LICENSE`](LICENSE).
