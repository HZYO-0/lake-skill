# BondLens 关系镜 — Codex Review Document

## 项目概述

**名称**：BondLens 关系镜
**版本**：0.1.0
**类型**：ChatGPT/Claude Custom Skill + Python CLI 工具
**定位**：基于证据的亲密关系沟通分析工具

### 核心理念

- **证据型分析**：每个结论必须有证据 ID、置信度、反证、替代解释
- **假设而非诊断**：使用"呈现...信号"，而非"就是...型"
- **隐私优先**：原始数据可选本地处理，只上传脱敏摘要
- **伦理边界**：禁止操控建议、临床诊断、确定性断言

---

## 架构

### 两种使用模式

**模式 1：直接使用 Skill（推荐，3 分钟部署）**
```
用户 → 安装 skills/bondlens 或创建 ChatGPT GPT → 粘贴 SKILL.md/上传框架文件 → 粘贴聊天记录 → 获得分析
```

**模式 2：CLI 预处理 + Skill 分析（增强隐私）**
```
用户 → CLI 本地预处理 → 生成脱敏摘要/证据索引 → 上传到 ChatGPT/Claude → 获得分析
```

### 数据流

**模式 1（直接粘贴）**：
```
用户复制聊天记录 → 粘贴到 Skill 对话框 → Skill 直接分析 → 输出报告 + 教练对话
```

**模式 2（CLI 预处理）**：
```
聊天记录（CSV/TXT/SQLite/SRT）
    ↓ bondlens ingest
标准化消息（JSONL）
    ↓ bondlens redact
脱敏消息（JSONL）
    ↓ bondlens segment
会话切分（JSONL）
    ↓ bondlens digest + bondlens evidence
摘要（MD）+ 证据索引（JSONL）
    ↓ bondlens export --mode conversations
完整对话（JSONL，脱敏文本）
    ↓ bondlens kb init
知识库（YAML/MD/JSONL）
    ↓ 上传到 ChatGPT/Claude
AI 教练对话
```

---

## 技术栈

- **语言**：Python 3.9+
- **CLI 框架**：Typer + Rich
- **数据模型**：Pydantic v2
- **测试**：pytest（26 个测试：23 unit/safety + 3 integration，全部通过）
- **代码质量**：ruff（lint，阻断）、mypy（类型检查，advisory）、bandit（安全扫描）
- **CI 安全**：隐私泄露扫描 + 禁止网络调用扫描（均为阻断项）

### 依赖

```
pydantic >= 2.7
typer >= 0.12
rich >= 13.7
python-dateutil >= 2.9
PyYAML >= 6.0
```

---

## Skill 能力

### 8 项分析输出

1. 关系画像报告
2. 非临床人格信号报告（大五人格维度）
3. 依恋焦虑/回避假设报告
4. 互动模式分析（正向/负向循环）
5. 沟通手册（场景化建议）
6. 多语气消息草稿（温和/直接/降压/有边界）
7. 知识库文件或增量补丁
8. 不确定性与安全说明

### 数据充分性评估

Skill 会根据输入数据量决定分析深度：

| 输入量 | 分析结果 |
|--------|---------|
| 少于约 30 条、单会话、缺少一方 | 仅低置信局部观察，不输出完整画像 |
| 多场景代表性聊天（推荐） | 完整 8 项分析，置信度合理 |
| CLI 脱敏导出 | 完整分析 + 知识库，适合隐私敏感场景 |

### 首次校准向导

数据不足时，Skill 会先问 4-5 个问题（关系类型、分析目标、数据量等），再进行分析。用户可跳过，跳过后仅输出低置信局部观察。

### 教练对话模式

- **开场**：总结 2-3 个发现 → 问"你想先聊哪个方面？"
- **探索**：引用证据 ID → 置信度 → 替代解释 → 具体建议
- **修正**：用户纠正 → 承认局限 → 更新假设
- **指导**：用户问"我该怎么说？"→ 3 种语气草稿 + 推理
- **收尾**：总结 + 未解决问题

### 8 个分析框架

| 框架 | 用途 |
|------|------|
| `evidence_ladder.md` | 5 级断言层级（事实→模式→假设→建议→象征） |
| `big_five_communication_signals.md` | 大五人格沟通信号（非临床） |
| `attachment_anxiety_avoidance.md` | 依恋焦虑/回避信号 |
| `relationship_communication_patterns.md` | 互动模式（正向/负向循环） |
| `forbidden_overclaims.md` | 禁止的过度断言清单 |
| `symbolic_mode_policy.md` | 星座/塔罗策略（默认关闭） |
| `coaching_dialogue_framework.md` | 教练对话方法论 |

---

## CLI 功能

### 9 个命令

| 命令 | 功能 | 输入 | 输出 |
|------|------|------|------|
| `bondlens init` | 初始化项目 | 路径 | 目录结构 |
| `bondlens ingest` | 导入聊天数据 | CSV/TXT/JSONL/SQLite/SRT/OCR | 标准化 JSONL |
| `bondlens redact` | 隐私脱敏 | JSONL | 脱敏 JSONL |
| `bondlens check-leaks` | 扫描隐私泄露 | 目录 | 报告 |
| `bondlens segment` | 会话切分 | JSONL | 会话 JSONL |
| `bondlens digest` | 生成摘要 | 消息+会话 | Markdown |
| `bondlens evidence` | 生成证据索引 | 消息+会话 | JSONL |
| `bondlens export` | 导出对话（3 种模式） | 消息+会话 | JSONL |
| `bondlens kb init/patch` | 知识库管理 | 消息+会话+证据 | 目录/补丁 |

### 导出模式

| 模式 | 内容 | 用途 |
|------|------|------|
| `summary` | 仅统计和摘要 | 最小上传 |
| `conversations` | 完整对话序列（脱敏文本） | 平衡隐私与分析质量 |
| `full` | 包含原始消息 | 仅本地使用 |

### 输入格式适配器（7 个）

| 适配器 | 格式 | 说明 |
|--------|------|------|
| `GenericCSVAdapter` | CSV | 通用 CSV，支持中英文列名 |
| `WeChatTXTAdapter` | TXT | 微信导出格式 |
| `GenericJSONLAdapter` | JSONL | 标准 JSONL |
| `WeChatSQLiteAdapter` | SQLite | 微信明文数据库（自动 schema 探测） |
| `VoiceTranscriptAdapter` | SRT/VTT | 语音转写（保留 ASR 置信度） |
| `OCRTranscriptAdapter` | JSONL/CSV | OCR 转写（保留 OCR 置信度） |
| `SQLiteInspector` | SQLite | 自动探测表结构 |

### 隐私模式（4 种）

| 模式 | 脱敏级别 | 用途 |
|------|---------|------|
| `local-raw` | 无脱敏 | 仅本地使用 |
| `local-safe` | 脱敏联系方式和 ID | 本地分享 |
| `cloud-safe` | 全面脱敏（姓名/组织/地点/时间粗化） | 上传到 AI |
| `publish-safe` | 仅合成数据 | 公开发布 |

---

## 测试

### 测试套件（26 个测试）

```
tests/
├── unit/
│   ├── test_simple.py            # 基础功能
│   ├── test_csv_adapter.py       # CSV 适配器
│   ├── test_txt_adapter.py       # TXT 适配器
│   ├── test_redaction.py         # 脱敏功能
│   ├── test_segmentation.py      # 会话切分
│   └── test_evidence_index.py    # 证据索引
├── integration/
│   └── test_cli_pipeline.py      # 完整 CLI pipeline（ingest→export）
└── safety/
    ├── test_privacy_leakage.py   # 隐私泄露测试
    └── test_no_decryption_behavior.py  # 不解密测试
```

### 验证状态

- 全部 26 个测试通过（23 unit/safety + 3 integration）
- Integration test 覆盖完整 pipeline：ingest → redact → segment → digest → evidence → export
- 隐私扫描：cli/ 和 skills/ 源码无真实隐私数据泄露
- 网络调用扫描：cli/ 和 skills/ 无禁止的网络调用
- 无解密行为

---

## 部署方式

详细安装指南见 [`INSTALL.md`](INSTALL.md)。

### 方式 1：ChatGPT 自定义 GPT（推荐，3 分钟）

1. 打开 ChatGPT → Create a GPT
2. 粘贴 `skills/bondlens/SKILL.md` 到 Instructions
3. 上传 `skills/bondlens/references/frameworks/` 下的 7 个文件到 Knowledge
4. 直接粘贴聊天记录开始使用

### 方式 2：Claude Code / Claude Project

- **Claude Project**：粘贴 `skills/bondlens/SKILL.md` 到 Instructions，上传框架文件到 Knowledge
- **Claude Code**：用 `npx skills add HZYO-0/bondlens -y`，或复制 `skills/bondlens/` 到 `.claude/skills/bondlens/`

### 方式 3：Codex / OpenCode

Codex 可用内置安装器安装 GitHub 子目录：

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo HZYO-0/bondlens \
  --path skills/bondlens
```

OpenCode 可复制 `skills/bondlens/` 到 `.opencode/skills/bondlens/`。

### 方式 4：CLI 本地预处理 + Skill（增强隐私）

```bash
git clone https://github.com/HZYO-0/bondlens.git && cd bondlens
pip install -e ".[dev]"
bondlens init ./my-project && cd my-project
bondlens ingest --file input/chat.csv --type csv --self-name 我 --target-name 对方
bondlens redact --file work/raw_messages.jsonl --out work/messages.redacted.jsonl
bondlens segment --file work/messages.redacted.jsonl --out work/sessions.redacted.jsonl
bondlens digest --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --out work/digest.redacted.md
bondlens evidence --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --out work/evidence.redacted.jsonl
bondlens export --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --out work/conversations.jsonl --mode conversations
bondlens kb init --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --evidence work/evidence.redacted.jsonl --out kb/
# 把 work/ 和 kb/ 中的文件上传到 ChatGPT/Claude
```

---

## 安全与伦理

### 禁止行为

- 解密微信数据库或绕过访问控制
- 临床诊断（人格障碍、依恋障碍、心理健康诊断）
- 操控建议（PUA、情感勒索、诱导嫉妒、冷暴力测试）
- 确定性断言（"他一定是..."、"他肯定..."）
- 预测关系结局

### 安全措施

- 4 种隐私模式，原始数据可选不上传
- PII 脱敏（手机号、身份证、邮箱、银行卡、微信号等）
- 泄露检查器（CI 集成）
- 禁忌清单（`forbidden_overclaims.md`）
- Prompt injection 防护（聊天记录视为数据，非指令）
- 不解密、不越权、不绕过保护

---

## CI/CD

### 工作流（4 个）

| 工作流 | 触发条件 | 阻断项 | 说明 |
|--------|---------|--------|------|
| `ci.yml` | push/PR to main | ruff lint + pytest（26 个） + 隐私扫描 | mypy 为 advisory |
| `security.yml` | push/PR + weekly | bandit + pip-audit + 网络调用扫描 | |
| `package-skill.yml` | push to main + tags | 打包 skill.zip | |
| `release.yml` | push tags v* | 测试 + 打包 + GitHub Release | |

### CI 安全扫描

- **隐私扫描** (`tools/check_no_real_private_data.py`)：扫描 cli/、skills/ 源码和 Skill 包中的手机号、身份证、邮箱、银行卡、微信号等 PII 模式。tests/ 和 docs/ 使用更宽的安全示例 allowlist。
- **网络调用扫描** (`tools/check_no_forbidden_network_calls.py`)：扫描 cli/、skills/ 中的 requests/urllib/httpx/aiohttp/socket 调用，确保本地预处理工具和 Skill 包不外发数据。
- **mypy**：当前为 advisory（`continue-on-error`），以 `python tools/check.py` 的当前输出为准。

---

## 状态

- CLI 完整可用（9 个命令，26 个测试全部通过）
- Skill 定义完整（`skills/bondlens/SKILL.md` + 7 个框架 + 首次校准向导 + 教练对话模式）
- 文档完整（README + INSTALL.md + chat_record_preparation.md + privacy_model + platform_compatibility + codex_setup）
- 多平台安装支持（ChatGPT/Claude/Codex/OpenCode/OpenClaw/Agents）
- CI/CD 配置完成（4 个 workflow，隐私扫描和网络调用扫描为阻断项）
- 示例数据完整（合成聊天记录 + 预期输出）
- mypy 类型检查当前为 advisory（非阻断），以 `python tools/check.py` 的当前输出为准
- `python tools/package_skill.py` 生成 6 个平台安装包
