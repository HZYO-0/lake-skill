# Project Spec: WeChat Relationship Insight

## 1. 项目目标

`wechat-relationship-insight` 是一个面向亲密关系聊天记录的证据型分析项目。它将用户合法持有的微信或其他聊天记录，在本地归一化、脱敏、切分、摘要和证据索引，然后交给 ChatGPT Skill 生成亲密关系画像、人格/依恋信号假设、互动模式分析、沟通建议和知识库更新。

项目不是：

- 微信数据库破解工具。
- 情感操控工具。
- 心理诊断工具。
- 星座/塔罗预测工具。
- 自动监控或自动发送消息工具。

## 2. 默认模式

默认模式：**本地预处理 + ChatGPT Skill 分析**。

```text
Raw inputs stay local as much as possible.
Only redacted digest, session summaries, evidence index, and optional existing KB are sent to ChatGPT.
```

默认上传文件：

```text
work/relationship_digest.redacted.md
work/session_summaries.redacted.jsonl
work/evidence_index.redacted.jsonl
kb/metadata.yaml
kb/*.md, if user has existing knowledge base
```

默认不上传：

```text
原始 .db
原始 .csv/.txt/.html
原始语音
原始截图
完整未脱敏聊天全文
```

## 3. 用户场景

### 3.1 暧昧关系分析

用户希望知道对方是否更偏靠近、回避、试探、保持距离，以及下一步如何推进而不制造压力。

输出：

- 暧昧阶段判断。
- 对方沟通偏好。
- 对方回应积极/冷淡场景。
- 低风险推进话术。

### 3.2 恋人关系复盘

用户希望从聊天记录中识别双方冲突循环、修复方式、误解来源和后续沟通方式。

输出：

- 正向循环与负向循环。
- 冲突触发点。
- 修复路径。
- 边界表达话术。

### 3.3 前任/复联场景

用户希望分析分手后互动、复联风险、对方边界和自己的表达是否压迫。

输出：

- 复联风险评估。
- 是否存在明确拒绝或边界信号。
- 尊重边界的沟通建议。
- 停止推进/降频建议。

### 3.4 长期知识库维护

用户持续导入新聊天记录，希望更新旧画像，而不是每次重新分析。

输出：

- `kb_patch.md`
- 新增观察。
- 强化观察。
- 修正旧判断。
- 反证。
- 未解决问题。

## 4. 输入范围

### 4.1 微信数据库

支持可读取明文 SQLite：

```text
.db
.sqlite
.sqlite3
```

要求：

- 用户合法持有。
- 数据库已经可读取。
- 项目不解密。
- 项目不提取密钥。
- 项目不绕过设备/账号/App 权限。

### 4.2 聊天导出文件

支持：

```text
.csv
.tsv
.txt
.md
.html
.htm
.json
.jsonl
```

### 4.3 语音转文字

支持：

```text
.srt
.vtt
.txt
.csv
.json
.jsonl
```

语音转写必须保留：

- `asr_confidence`
- `duration_sec`
- `transcript_source`
- `source_audio`
- `quality.note`

### 4.4 OCR/媒体转文字

支持用户提供的 OCR 或字幕结果：

```text
ocr_transcript.jsonl
screenshot_text.csv
video_subtitle.srt
```

OCR/ASR 内容只作为派生证据，必须保留置信度和来源。

## 5. 输出范围

### 5.1 报告

```text
reports/profile_report.md
reports/personality_signals.md
reports/attachment_hypotheses.md
reports/interaction_patterns.md
reports/communication_playbook.md
reports/reply_drafts.md
reports/kb_patch.md
```

### 5.2 知识库

```text
kb/
├── README.md
├── metadata.yaml
├── target_profile.md
├── attachment_hypotheses.md
├── personality_signals.md
├── interaction_patterns.md
├── relationship_timeline.md
├── communication_playbook.md
├── reply_style_guide.md
├── unresolved_questions.md
├── evidence_index.jsonl
└── update_log.md
```

## 6. 核心质量标准

每个重要分析结论必须具备：

```text
观察
证据 ID
推断
置信度
反证
替代解释
沟通建议
```

示例：

```markdown
### 观察
对方在关系定义话题升温后，3 次出现延迟回应或转移话题。

### 证据
E-20250521-003, E-20250528-011, E-20250602-004

### 推断
这可能表示对方在高压力亲密议题中存在回避沟通信号。

### 置信度
中。模式跨多个会话出现，但不能判断完整人格。

### 反证
E-20250610-002 显示对方也曾主动解释自己的感受，因此不能说对方总是回避。

### 替代解释
近期压力、表达能力限制、关系阶段不明确、用户追问方式较强。

### 沟通建议
先降低压力，再约定具体时间复盘；避免连续追问。
```

## 7. 产品边界

禁止：

- 解密微信数据库。
- 越权读取他人聊天记录。
- 自动监控聊天。
- 自动发送消息。
- 输出临床诊断。
- 输出人格障碍判断。
- 输出操控、PUA、冷暴力测试、诱导嫉妒、威胁、骚扰建议。
- 用星座/塔罗作为核心证据。

允许：

- 证据型沟通画像。
- 非临床人格信号假设。
- 依恋焦虑/回避沟通信号假设。
- 互动模式分析。
- 尊重边界的沟通建议。
- 消息草稿改写。
- 知识库更新。
