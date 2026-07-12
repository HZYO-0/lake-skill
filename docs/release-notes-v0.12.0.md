# LakeSkill 0.12.0 Release Notes

> **发布主题**：从「能跑通」到「可信可审」——固定分析链路，把候选与结论分离。

这是 LakeSkill 第一次发布到 PyPI 的正式版本。0.12 把分析链路做成 6 个明确阶段：原始聊天 → 全量候选 → Skill 语义决策 → 正式台账 → 统一分析 JSON → Markdown / 本地 HTML。每一步的产物都是磁盘上的 JSONL 或 JSON，便于回放和审计。

---

## 1. 分析链路产品化（最核心变化）

| 阶段 | 命令 / 模块 | 产物 |
|---|---|---|
| 1. 原始聊天 → 标准化消息 | `ingest` | `work/raw_messages.jsonl` |
| 2. 隐私脱敏 | `redact` | `work/messages.redacted.jsonl` |
| 3. 会话切片 | `segment` | `work/sessions.jsonl` |
| 4. 关系信号**高召回候选** | `signals` | `work/relationship_signal_candidates.jsonl` |
| 5. Skill 语义决策（confirmed / downgraded / excluded） | `signals-finalize` | `work/relationship_signal_ledger.jsonl` + `relationship_analysis.json` |
| 6. 人类可读报告 | — | `relationship_analysis.md` / `.html` |

一站式流水线：

```bash
lake-skill process --file examples/synthetic_input/chat.csv --out work
```

它会自动跑：ingest → redact → segment → digest → evidence → intake → doctor → export → bundle。

---

## 2. 新增 CLI 命令

| 命令 | 作用 |
|---|---|
| `lake-skill start` | 引导式首跑，自动建隔离 contact workspace |
| `lake-skill process` | 一条命令完成导入、脱敏、切片、证据提取、候选提取、统计和 bundle |
| `lake-skill signals` | 抽取**高召回**关系信号候选（结论在此阶段**故意延后**） |
| `lake-skill signals-finalize` | 审计 Skill 决策、保留 excluded、生成正式台账和统一分析 |
| `lake-skill route` | 跨平台文本路由（`/急 /深度 /画像 /复盘 /更新 /改写`） |
| `lake-skill doctor` | 数据就绪度检查 → `data_readiness.md` |
| `lake-skill intake` | 生成 intake 卡片（关系类型/状态/数据源/隐私模式） |
| `lake-skill bundle` | 收集可上传的脱敏产物 + `upload_readme.md` |
| `lake-skill demo` | 生成公开可发的合成 demo 包 |
| `lake-skill report-lint` | 报告 lint：风险词、缺失层、弱结论格式 |
| `lake-skill audit` | 关系信号可靠性审计 |
| `lake-skill version` | 显示版本 |
| `lake-skill check-leaks` | 目录级隐私泄露扫描 |
| `lake-skill export` | 三档导出：`summary` / `conversations` / `full` |
| `lake-skill kb init` / `kb patch` | 知识库初始化与增量更新 |

---

## 3. 候选-决策-台账三层分离

- **候选**（`RelationshipSignalCandidate`）：高召回，模式匹配出的可能信号。置信度不等于关系结论。
- **决策**（`RelationshipSignalDecision`）：Skill 给出 `confirmed` / `downgraded` / `excluded` 之一，并填写 `event_id, tier, decision_reason, consensus_state, boundary_effect, conditions, counterevidence_ids, must_not_infer`。
- **台账**（`RelationshipSignalLedgerEntry`）：所有 excluded 也必须保留，**禁止静默遗漏**。

`signals-finalize` 会审计 Skill 决策、校验 schema，并产出**唯一事实源** `relationship_analysis.json`，下游报告必须以它为依据。

---

## 4. 证据优先级硬约束（T1–T4）

- **T1**：双方关于关系定义、拒绝、暂停、条件、边界、承诺、分手、复合、修复的**明确原话**。
- **T2**：跨 session 的稳定互动模式与兑现情况。
- **T3**：单一 session 的情境性行为。
- **T4**：消息量、回复时间、长度、发起比例等描述统计。

**T1 永远高于 T4**。回复快、消息多、继续日常聊天，都不能推翻明确拒绝或边界。

事件确认时强制检查：触发原话 + 说话人 + 同 session 前 2 / 后 4 条 + 对方即时回应 + 双方定义 + 条件 + 责任主体 + 后续 3 个 session / 14 天内跟进 + 改口 + 兑现 + 撤回 + 反证。

---

## 5. Skill 行为规约（`skills/lake-skill/SKILL.md`）

- **输入路由**：`/急` → 1 分钟行动卡；`/深度` → 完整报告；`/画像` → 双方画像；`/复盘` → 阶段比较；`/更新` → 知识库增量；`/改写` → 边界检查 + 消息草稿。
- **强制数据顺序**：候选 → 决策 → finalize → 唯一事实源 → 关系讨论 → 行动卡 → 画像 → 互动统计。
- **报告顺序硬约束**（8 段固定）：关键关系讨论 → 已有共识 → 分歧与开放条件 → 最近改口/阶段变化 → 可判断与不可判断 → 本周行动/避免/消息草稿 → 双方画像/互动模式/依恋假设 → 不确定性与反证。
- **禁止过度推断**：「不是不喜欢你，只是不想现在开始」不得压成单纯接受或拒绝；「我朋友要结婚了」不得升级为双方未来承诺；「不合适」不得解释为等待挽留。

---

## 6. 描述性互动统计（永远 T4 上下文）

`interaction_stats.py` 计算：双方消息量、发起比例、回复时间分布、连续发言 streaks、长间隔等。**只作为背景，不作为关系分数**。

配合 `analysis_windows.py` 实现「关系讨论候选**全量前置** + 其它窗口按优先级采样」，确保重要对话永不被采样掉。

---

## 7. 多平台分发

`tools/package_skill.py` 把 `skills/lake-skill/` 打包成 6 个平台格式：

| 平台 | 路径 |
|---|---|
| ChatGPT Custom GPT | `dist/chatgpt/`（SKILL.md + frameworks） |
| Claude | `dist/claude/.claude/skills/lake-skill/` |
| Codex | `dist/codex/.codex/skills/lake-skill/` |
| OpenCode | `dist/opencode/.opencode/skills/lake-skill/` |
| OpenClaw | `dist/openclaw/.openclaw/workspace/skills/lake-skill/` |
| Agents | `dist/agents/.agents/skills/lake-skill/` |

`tools/sync_skill_copies.py` 用 SHA-256 manifest 同步项目内 4 个本地副本，防止平台拷贝漂移。

---

## 8. 隐私与安全

- `privacy_mode` 三档：`local-raw` / `local-safe` / `cloud-safe`，`process` 强制校验。
- `lake-skill check-leaks <dir>` 在打包前扫真实数据残留。
- CI 与 Security workflow 检查 `mimocode/`、`.codex-global-state` 等真实数据是否被 `.gitignore`。
- 公开 demo 全部**合成数据**，明确标注「do not replace with private analyses」。

---

## 9. 安装与首发

```bash
pip install lake-skill
lake-skill version    # 0.12.0
lake-skill demo --out examples/social_demo
lake-skill start
```

PyPI 首次发布（`lake-skill 0.12.0`），GitHub Release 同号。

---

## 10. 测试覆盖

新增关系信号与产品化专项测试：

- `tests/unit/test_productization.py`：打包、同步、入口脚本、跨平台 schema。
- `tests/unit/test_relationship_signals.py`：候选抽取、决策、台账、反证、边界效应。
- `tests/unit/test_prompts.py`：SKILL 路由与强制顺序。

---

## 11. 致谢与下一步

- 下一版本（0.13）将聚焦：**关系时序可视化**、**多角色多 contact 跨段对比**、**改写模板与边界检查的更细粒度反馈**。
- 欢迎提交 issue / PR。**不要把真实聊天贴到 issue**——只贴脱敏后的 `relationship_signal_ledger.jsonl` 与报告产物。

— LakeSkill 0.12.0
