# 常见问题 (FAQ)

## 安装与环境

### 需要什么环境？

- **Python 3.9+**（推荐 3.11）
- **AI Agent 运行时**（任选一个）：Codex、Claude Code、OpenCode、ChatGPT

如果只用 CLI 预处理，只需要 Python。如果要让 AI 分析聊天记录，需要一个 AI Agent 运行时。

### 怎么安装？

最快的方式：

```bash
npx skills add HZYO-0/lake-skill -y
```

或用 pip：

```bash
pip install lake-skill
```

更多安装方式见 [INSTALL.md](../INSTALL.md)。

### 安装后怎么验证？

```bash
lake-skill version
```

应该看到 `lake-skill v0.10.0`。

---

## 隐私与安全

### 聊天记录安全吗？

LakeSkill 默认使用 `cloud-safe` 隐私模式，会自动脱敏：
- 手机号、身份证号、银行卡号
- 姓名、组织、地址
- 微信号、邮箱

你可以选择 `local-safe` 模式，只脱敏高风险信息；或 `local-raw` 模式，不脱敏（仅限本地使用）。

### 聊天记录会被上传到服务器吗？

**不会。** LakeSkill 本身不联网，不上传任何数据。数据处理完全在本地完成。

当你使用 AI Agent（如 ChatGPT、Claude）分析时，脱敏后的数据会发送给 AI 服务。这是你主动操作的行为，不是 LakeSkill 自动上传的。

### 我可以用真实聊天记录做公开分享吗？

**不行。** 公开展示（小红书、抖音、README 等）只能使用合成数据：

```bash
lake-skill demo --out examples/social_demo
```

这会生成完全虚构的聊天数据，不包含任何真实信息。

### 加密的微信数据库能直接读取吗？

**不能。** LakeSkill 明确拒绝处理加密数据库。你需要先用 [WeChatDataAnalysis](https://github.com/LifeArchiveProject/WeChatDataAnalysis) 解密你自己的微信数据库，然后导出为 CSV/TXT/JSON 格式再导入。

---

## 使用方法

### 支持哪些聊天记录格式？

| 格式 | 说明 |
|------|------|
| CSV | 通用格式，多数导出工具默认 |
| TXT | 微信聊天记录导出格式 |
| JSONL | 结构化 JSON |
| SQLite | 解密后的微信数据库 |
| SRT/VTT | 语音转文字结果 |
| 直接粘贴 | 纯文本，最快的方式 |

### 怎么快速试一下？

安装好 Skill 后，直接粘贴一段聊天记录给 AI：

```text
使用 lake-skill，帮我分析这段聊天记录。先给行动卡。

[2026-06-01 22:13] 我: 最近感觉你有点少回我
[2026-06-01 22:18] TA: 没有，就是这几天事情比较多
```

### 一键处理命令是什么？

```bash
lake-skill process --file chat.csv --out work
```

这会自动执行：导入 → 脱敏 → 分段 → 摘要 → 证据索引 → 数据体检 → 导出 → 打包。

### 证据 ID 是什么？

每条分析判断都会标注一个证据 ID（如 `E-20260601-001`），对应聊天记录中的具体原文。你可以追溯每条结论的来源。

如果没有证据 ID，说明这条判断是 AI 的猜测，不是基于证据的结论。

### 分析结果准确吗？

LakeSkill 不追求"准确"——它追求**有证据支撑**。

- 证据充分时：给出中高置信度的结论
- 证据不足时：明确降级，只给低风险观察
- 每条结论都附带反证和替代解释

它不会告诉你"TA 喜欢你"或"TA 不喜欢你"，而是告诉你"证据支持什么、不支持什么"。

---

## 与其他工具的区别

### 和直接用 ChatGPT 分析有什么区别？

| | ChatGPT 直接分析 | LakeSkill |
|---|---|---|
| 结论风格 | 倾向给肯定答案 | 证据不够就降级 |
| 证据追溯 | 无 | 每条判断有证据 ID |
| 隐私保护 | 聊天记录直接发送 | 先本地脱敏再上传 |
| 反证 | 通常没有 | 每条结论有反证 |
| 行动建议 | 泛泛而谈 | 具体到"本周做什么" |

### 和其他聊天分析工具有什么区别？

LakeSkill 的核心差异：
1. **不猜心**：不告诉你 TA 爱不爱你，只整理证据
2. **隐私优先**：4 级隐私模式，数据不出本地
3. **反操控**：不提供 PUA 策略、挽回技巧
4. **开源透明**：所有分析逻辑都可以审查

---

## 贡献与反馈

### 发现 Bug 怎么办？

在 [GitHub Issues](https://github.com/HZYO-0/lake-skill/issues) 提交，选择 "Bug Report" 模板。

### 想提功能建议？

在 [GitHub Issues](https://github.com/HZYO-0/lake-skill/issues) 提交，选择 "Feature Request" 模板。

### 想参与开发？

见 [CONTRIBUTING.md](../CONTRIBUTING.md)。
