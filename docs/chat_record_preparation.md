# 聊天记录准备指南

## 第一次有效分析需要什么

| 条件 | 最低要求 | 推荐 |
|------|---------|------|
| 消息数量 | ~30 条 | 100+ 条 |
| 时间跨度 | 数天 | 数周到数月 |
| 双方发言 | 至少各 5 条 | 双方均衡 |
| 场景覆盖 | 1-2 种 | 5+ 种（日常、冲突、修复、邀约、冷淡、升温） |

数据越丰富，结论越稳定。少量片段只能做低置信局部观察。

---

## 三种导入方式

### A. 直接粘贴（最快，适合试用）

直接把聊天记录粘贴到对话框：

```
以下是我和某人的聊天记录，请帮我分析：

2025-05-21 22:13 张三: 今天其实有点想你
2025-05-21 22:14 我: 真的吗？我也在想你
...
```

- 优点：零门槛，立即开始
- 缺点：数据经过平台，适合快速试用

### B. 上传文件（适合较长记录）

支持格式：
- **TXT**：微信电脑版导出格式
- **CSV**：通用表格格式（需包含时间、发送者、内容列）
- **JSONL**：结构化数据

```
请帮我分析这个聊天记录文件：[上传 chat.txt 或 chat.csv]
```

### C. CLI 本地预处理（隐私优先）

适合隐私敏感或数据量大的场景。原始数据不出本地，只上传脱敏摘要。

```bash
# 安装 CLI
pip install -e ".[dev]"

# 完整 pipeline
bondlens init ./my-project && cd my-project
bondlens ingest --file input/chat.csv --type csv --self-name 我 --target-name 对方
bondlens redact --file work/raw_messages.jsonl --out work/messages.redacted.jsonl
bondlens segment --file work/messages.redacted.jsonl --out work/sessions.redacted.jsonl
bondlens digest --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --out work/digest.redacted.md
bondlens evidence --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --out work/evidence.redacted.jsonl
bondlens export --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --out work/conversations.jsonl --mode conversations
bondlens kb init --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --evidence work/evidence.redacted.jsonl --out kb/
```

上传以下文件到 Skill：
- `work/digest.redacted.md`
- `work/sessions.redacted.jsonl`
- `work/evidence.redacted.jsonl`
- `work/conversations.jsonl`
- `kb/*.md`（如有）

---

## 推荐提供的场景

分析越准，需要覆盖的场景越多：

| 场景 | 为什么重要 |
|------|-----------|
| 日常聊天 | 基线沟通风格 |
| 邀约/计划 | 主动性和投入度 |
| 冲突/争吵 | 冲突模式和升级路径 |
| 修复/道歉 | 修复能力和安全依恋信号 |
| 冷淡/回避 | 回避模式和边界信号 |
| 升温/暧昧 | 情感表达和推进节奏 |
| 边界讨论 | 边界表达和尊重程度 |

---

## 微信聊天记录导出

- 微信电脑版 → 右键聊天 → 导出聊天记录 → 选择 TXT 或 CSV
- 或使用第三方导出工具

---

## 不支持

- 解密微信数据库
- 绕过访问控制
- 抓取对方未授权的数据
- 处理原始截图/图片（只分析 OCR 转写文本）
