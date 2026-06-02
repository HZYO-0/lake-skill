# BondLens 关系镜

基于证据的亲密关系沟通分析 Skill/Agent。

不是"他就是回避型"，而是"聊天记录呈现回避相关信号，置信度中等，替代解释包括……"。

## 快速开始

### 1. 创建 Skill/Agent

在 ChatGPT、Claude、Codex 或其他支持 Skill/Agent 的平台创建一个新的 Skill/Agent。

### 2. 粘贴指令

把 [`skill/SKILL.md`](skill/SKILL.md) 的全部内容复制粘贴到指令（Instructions）框中。

### 3. 上传知识文件

把 [`skill/references/frameworks/`](skill/references/frameworks/) 目录下的 7 个 `.md` 文件上传为附加知识/上下文：

```
skill/references/frameworks/
├── evidence_ladder.md                    # 证据等级定义
├── big_five_communication_signals.md     # 大五人格沟通信号
├── attachment_anxiety_avoidance.md       # 依恋焦虑/回避信号
├── relationship_communication_patterns.md # 关系互动模式
├── forbidden_overclaims.md               # 禁止的过度断言
├── symbolic_mode_policy.md               # 星座/塔罗策略
└── coaching_dialogue_framework.md        # 教练对话框架
```

### 4. 导入聊天记录完成首次校准

直接粘贴或上传你的聊天记录。首次分析需要**足量、有代表性**的聊天记录才能给出完整画像。

**输入质量与分析深度**：

| 输入量 | 分析结果 |
|--------|---------|
| 5-10 条片段 | 仅低置信局部观察，不输出完整画像 |
| 多场景代表性聊天（推荐） | 完整 8 项分析，置信度合理 |
| CLI 脱敏导出 | 完整分析 + 知识库，适合隐私敏感场景 |

**粘贴示例**：

```
以下是我和某人的聊天记录，请帮我分析：

2025-05-21 22:13 张三: 今天其实有点想你
2025-05-21 22:14 我: 真的吗？我也在想你
2025-05-21 22:15 张三: 嗯嗯，最近工作有点累
2025-05-21 22:16 我: 辛苦了，周末要不要一起吃饭
...
（建议包含多个时间段、多种场景的聊天记录）
```

---

## 它能做什么

### 分析输出（8 项）

1. **关系画像** — 整体关系状态概述
2. **人格信号** — 非临床的沟通风格分析（大五人格维度）
3. **依恋假设** — 焦虑/回避/安全型信号，附替代解释
4. **互动模式** — 正向循环、负向循环、冲突升级路径
5. **沟通手册** — 针对日常聊天、暧昧推进、冲突修复等场景的建议
6. **消息草稿** — 温和版/直接版/降压版/有边界版
7. **知识库** — 可持续更新的关系档案（增量补丁，不覆盖旧判断）
8. **不确定性说明** — 每个结论的置信度、反证、替代解释

### 教练对话

- **开场**：总结 2-3 个发现，问"你想先聊哪个方面？"
- **探索**：引用证据 → 置信度 → 替代解释 → 具体建议
- **修正**：你说"他不会那样做"→ 承认局限 → 更新理解
- **指导**：你问"我该怎么说？"→ 3 种语气草稿 + 推理

---

## 支持的输入方式

| 方式 | 说明 | 隐私级别 |
|------|------|---------|
| **直接粘贴** | 在对话框粘贴聊天记录 | 低（数据经过平台） |
| **上传文件** | 导出聊天记录文件上传 | 低（数据经过平台） |
| **CLI 预处理** | 本地脱敏后上传摘要（见下方） | 高（原始数据不出本地） |

### 支持的数据源

| 数据源 | 格式 | 说明 |
|--------|------|------|
| 微信电脑版导出 | TXT/CSV | 右键聊天 → 导出聊天记录 |
| 通用 CSV | CSV | 需包含时间、发送者、内容列 |
| JSONL | JSONL | 结构化消息数据 |
| 微信明文数据库 | SQLite | `.db` 文件（不解密加密数据库） |
| 语音转写 | SRT/VTT | 保留 ASR 置信度字段 |
| OCR 转写 | JSONL/CSV | 保留 OCR 置信度字段 |

详细说明见 [`docs/chat_record_preparation.md`](docs/chat_record_preparation.md)。

### 微信聊天记录导出

- 微信电脑版 → 右键聊天 → 导出聊天记录 → 选择 TXT 或 CSV
- 或使用第三方导出工具

---

## CLI 本地预处理（可选，增强隐私）

隐私敏感或数据量大时，可用 CLI 工具在本地预处理，只上传脱敏后的产物。

```bash
# 从源码安装（需要 Python 3.9+）
git clone https://github.com/HZYO-0/bondlens.git
cd bondlens
pip install -e ".[dev]"

bondlens init ./my-project && cd my-project

bondlens ingest --file input/chat.csv --type csv --self-name 我 --target-name 对方
bondlens redact --file work/raw_messages.jsonl --out work/messages.redacted.jsonl
bondlens segment --file work/messages.redacted.jsonl --out work/sessions.redacted.jsonl
bondlens digest --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --out work/digest.redacted.md
bondlens evidence --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --out work/evidence.redacted.jsonl
bondlens export --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --out work/conversations.jsonl --mode conversations
bondlens kb init --messages work/messages.redacted.jsonl --sessions work/sessions.redacted.jsonl --evidence work/evidence.redacted.jsonl --out kb/
```

然后把 `work/` 和 `kb/` 中的文件上传到 Skill/Agent。

---

## 与其他 Skill 的区别

| | colleague-skill | ex-skill | **本项目** |
|---|---|---|---|
| **核心体验** | 和"AI 版 TA"对话 | 和"前任"对话 | 理解关系 + 改善沟通 |
| **输出** | AI Persona | AI Persona | 分析报告 + 教练 + 草稿 |
| **分析依据** | 无证据 | 无证据 | 每个结论有证据 ID、置信度、反证 |
| **隐私** | 上传原始数据 | 上传原始数据 | 可选本地预处理 |
| **伦理边界** | 无明确限制 | 无明确限制 | 禁止操控、诊断、确定性断言 |

---

## 项目结构

```
├── cli/                          # Python CLI（可选，隐私增强）
│   └── bondlens/
│       ├── cli.py                # 命令行入口
│       ├── schema.py             # 数据模型
│       ├── adapters/             # 输入格式适配器
│       ├── privacy/              # 隐私脱敏
│       ├── segmentation/         # 会话切分
│       ├── evidence/             # 证据索引
│       ├── kb/                   # 知识库管理
│       └── reports/              # 报告生成
├── skill/                        # Skill/Agent 定义
│   ├── SKILL.md                  # 指令（粘贴到 Instructions）
│   ├── references/frameworks/    # 分析框架（上传为知识）
│   └── assets/kb_template/       # 知识库模板
├── tests/                        # 测试
├── examples/                     # 合成示例数据
└── docs/                         # 文档
```

## 验证

开发环境下的推荐验证命令：

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行全部检查（ruff + pytest + 隐私扫描 + 网络扫描）
python tools/check.py --quick

# 运行完整检查（含 mypy advisory）
python tools/check.py

# 仅运行测试
python -m pytest -q

# 打包 Skill（生成 dist/ 下的多平台安装包）
python tools/package_skill.py
```

## 当前限制

- **CLI 未发布到 PyPI**：`pip install bondlens` 暂不可用。需要从源码安装：`pip install -e ".[dev]"`
- **mypy 类型检查**：当前为 advisory 模式，0 errors
- **数据库解密**：不支持解密加密的微信数据库，仅支持明文 SQLite

## 许可证

MIT License
