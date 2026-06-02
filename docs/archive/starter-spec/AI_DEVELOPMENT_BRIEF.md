# AI Development Brief

> 把本文件作为 AI coding agent 的项目上下文。开发时必须遵守这里的产品边界、默认部署模式、隐私策略、分析框架和测试要求。

## 1. 项目名称

`wechat-relationship-insight`

中文名：微信亲密关系洞察助手。

## 2. 项目定位

开发一个隐私优先的本地预处理工具 + ChatGPT Skill，用于分析用户合法持有并主动提供的亲密关系聊天记录。支持微信可读取数据库、CSV/TXT/HTML/JSON/JSONL 导出、语音转文字结果、OCR/字幕/媒体转写结果，以及已有关系知识库。

项目输出：

- 对方亲密关系沟通画像报告。
- 非临床人格沟通信号报告。
- 成人依恋焦虑/回避相关信号假设。
- 双方互动循环分析。
- 后续沟通建议。
- 多风格消息草稿。
- 可持续更新的关系知识库和增量 patch。

## 3. 默认部署模式

默认必须实现并优化：

```text
local preprocessing + ChatGPT Skill analysis
```

也就是：

```text
原始微信数据库 / 聊天导出 / 语音转写 / OCR
        ↓ 本地 CLI
normalized_messages.jsonl
        ↓ 本地 cloud-safe 脱敏
normalized.cloud-safe.jsonl
        ↓ 本地会话切分、摘要、证据索引
session_summaries.redacted.jsonl
relationship_digest.redacted.md
evidence_index.redacted.jsonl
        ↓ 上传给 ChatGPT Skill
画像报告 / 依恋假设 / 人格信号 / 互动模式 / 沟通建议 / KB patch
```

不要把“直接上传原始聊天记录给 ChatGPT”作为默认路径。

## 4. 必须支持的输入

第一优先级：

- 可读取明文 SQLite：`.db`, `.sqlite`, `.sqlite3`
- CSV：`.csv`, `.tsv`
- 文本导出：`.txt`, `.md`
- HTML 导出：`.html`, `.htm`
- 通用 JSON/JSONL：`.json`, `.jsonl`
- 语音转文字：`.srt`, `.vtt`, `.txt`, `.jsonl`, `.csv`
- OCR/截图转文字：`.jsonl`, `.csv`, `.txt`

必须明确：项目不提供微信数据库解密、密钥提取、越权读取、绕过设备/账号/App 安全限制等功能。

## 5. 隐私模式

默认 `cloud-safe`。

实现四种模式：

```text
local-raw    完全本地、完全不脱敏，不允许上传
local-safe   本地使用，脱敏高风险标识符
cloud-safe   默认，上传给 ChatGPT Skill 前使用
publish-safe 公开示例、issue、测试 fixture，只允许合成数据
```

默认配置必须包含：

```yaml
privacy:
  default_privacy_mode: cloud-safe
  raw_upload_allowed: false
  upload_policy: digest_and_evidence_only
```

## 6. 核心分析原则

所有结论必须采用证据链：

```text
观察 → 证据 ID → 推断 → 置信度 → 反证 → 替代解释 → 沟通建议
```

不可输出：

- “对方就是回避型/焦虑型”。
- “对方一定爱你/不爱你”。
- “对方是某种人格障碍”。
- “用这段话让对方离不开你”。
- “让前任吃醋/刺激对方/冷暴力测试”。
- “塔罗/星座证明你们会复合”。

应该输出：

- “聊天记录呈现某些回避沟通信号”。
- “该判断置信度中等，替代解释包括……”。
- “建议以尊重边界、清晰表达和降压沟通为主”。

## 7. 人格与依恋框架

核心使用：

- Big Five 启发的人格沟通信号。
- 成人依恋的两个维度：依恋焦虑、依恋回避。
- 关系沟通循环：正向循环、负向循环、冲突升级、修复路径、连接请求与回应。

不要把人格/依恋框架当诊断工具。聊天记录只能支持“沟通信号假设”，不能支持真实人格诊断。

## 8. 星座、塔罗、占卜

默认禁用。

如未来支持，只能作为显式开启的 `symbolic-reflection` 模式：

- 只能用于自我反思、情绪表达、写日记问题。
- 不能影响人格/依恋/关系判断。
- 不能预测复合、命运、爱不爱。
- 必须明确标注“娱乐/象征反思，不是证据型判断”。

## 9. 首个 MVP 必须交付

MVP 目标：让用户能用合成数据跑通：

```text
CSV/TXT/SQLite/语音转写 → normalized_messages.jsonl → cloud-safe 脱敏 → session_summaries → digest → evidence_index → 上传 Skill → 输出报告与 KB patch
```

必须包括：

- CLI 基础框架。
- 标准 message schema。
- CSV/TXT/SQLite adapter。
- voice transcript adapter。
- privacy mode。
- segmentation。
- evidence index。
- digest。
- KB 模板。
- Skill `SKILL.md` 和 references。
- 单元测试、集成测试、安全测试。
- GitHub Actions CI。

## 10. 测试红线

以下测试必须通过：

- 加密/不可读取数据库不会尝试破解。
- 聊天记录中的 prompt injection 不会被执行。
- 输出不包含操控性建议。
- 输出不做临床诊断。
- 上传模式默认不输出原始聊天全文。
- `publish-safe` 不允许真实数据。
- 每个画像结论都有 evidence_id。
- 语音/OCR 低置信文本不会被当作高置信事实。
