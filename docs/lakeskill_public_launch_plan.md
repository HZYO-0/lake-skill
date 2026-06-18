# LakeSkill Public Launch Plan

本文件用于沉淀 LakeSkill 湖镜当前阶段的宣传、README 和功能改进计划。它面向后续复盘和迭代，不引用本地私有分析材料，公开演示只使用合成数据。

## 1. 当前目标

LakeSkill 需要同时服务两类用户：

1. 开发者和 agent 用户：可安装、可本地预处理、可审计的关系聊天分析 Skill。
2. 中文内容平台用户：不是替用户猜测对方真实想法，而是把聊天证据整理成行动卡、置信度和下一步建议。

主定位：

```text
别让 AI 猜 TA 爱不爱你。让 LakeSkill 告诉你：聊天证据支持什么、不支持什么、下一步怎么做更稳。
```

公开叙事必须强调：

- 不扮演对方。
- 不制造情感依赖。
- 不承诺关系结果。
- 不提供医疗、心理健康或未成年人亲密陪伴服务。
- 所有公开样例使用合成数据。

## 2. 宣传路径

冷启动顺序：

1. GitHub 和 Skill 目录先完成安装转化。
2. 小红书用图文和长图做中文破圈。
3. 抖音用 20-45 秒屏幕录制扩大认知。
4. 商业化只先围绕隐私优先的数据整理、本地部署、报告模板和工作流支持。

不建议现阶段做公开 Web/SaaS 情感互动产品。若未来面向中国境内公众提供持续性情感互动服务，需要重新做合规评估。

## 3. 小红书内容计划

内容矩阵：

- 系列 A：聊天过度解读纠偏。
- 系列 B：LakeSkill 工具教程。
- 系列 C：隐私安全和本地脱敏。
- 系列 D：反操控边界和安全使用。

首批 12 个题目：

1. TA 回得慢，只能说明一件事：证据还不够
2. 我做了一个不会替你上头的聊天分析工具
3. 把聊天记录交给 AI 前，先做这 3 步
4. 一段聊天能不能支持“关系变冷”的判断？
5. LakeSkill 湖镜：先给行动卡，再给长报告
6. 为什么聊天分析必须有置信度
7. 不要把一次短回复当作整段关系的答案
8. 用合成聊天演示：行动卡是怎么来的
9. 聊天记录太多？先做本地脱敏和数据体检
10. 我为什么不做情绪依赖型 AI 工具
11. 关系分析里，最重要的不是结论，是反证
12. 一个适合 Codex/Claude Code 的关系聊天 Skill

首批完整样稿已经放在 [promotion_plan.md](promotion_plan.md) 中，后续发布时只改封面和截图，不使用真实聊天。

## 4. 抖音内容计划

视频结构：

```text
3 秒痛点钩子 -> 15 秒行动卡演示 -> 10 秒证据 ID / 置信度解释 -> 5 秒安装口令
```

首批 8 条脚本方向：

1. AI 太肯定时，关系分析反而危险。
2. 一个不会替你上头的关系分析工具。
3. 聊天记录多，不等于证据足够。
4. 公开演示为什么只能用合成数据。
5. 一张行动卡应该回答什么。
6. 为什么必须展示反证和替代解释。
7. 给 Codex/Claude Code 装一个关系分析 Skill。
8. 上传前先本地脱敏、查漏、打包。

录屏 Demo：

- Demo A：GitHub README -> `lake-skill demo` -> 合成 CSV -> 行动卡 -> 证据 ID。
- Demo B：`doctor` -> 三档可分析程度 -> `bundle` -> upload readme。

## 5. README 改进方案

README 首屏需要在 30 秒内回答：

- 这是什么。
- 适合谁。
- 怎么试。
- 为什么可信。

改版原则：

1. 一句话定位和 30 秒 Demo 前置。
2. 三种使用路径前置：agent 用户、非技术用户、隐私敏感用户。
3. “为什么叫湖镜”后移，保留诗性但不压过安装与试用。
4. 把 `intake`、`doctor`、`demo`、`bundle` 写入核心流程。
5. 明确 `pip install -e ".[dev]"`，避免用户只运行 `pip install`。
6. 补充商业使用边界。
7. 清理公开文档和源码 docstring 里的旧品牌残留。

## 6. 功能改进路线

V0.10.1：

- `lake-skill demo`：一键生成合成聊天、脱敏产物、证据索引和行动卡示例。
- `lake-skill report-lint`：把报告检查脚本包进 CLI。
- `lake-skill audit`：把关系信号审计脚本包进 CLI。
- `doctor` 输出三档可分析程度：只能局部观察 / 可出行动卡 / 可出完整报告。

V0.10.2：

- `lake-skill bundle`：把上传所需文件打包成一个文件夹，并附 `upload_readme.md`。
- 安全模板：新增使用边界、数据同意、危机表达转介提示、未成年人限制说明。
- Bundle 风险提示：上传前确认脱敏、授权和危机场景边界。
- Demo 社交物料包：默认生成小红书长图文案、正文草稿、抖音录屏脚本和录屏检查清单。

## 7. 当前落地文件

文档：

- [README.md](../README.md)
- [README_EN.md](../README_EN.md)
- [INSTALL.md](../INSTALL.md)
- [promotion_plan.md](promotion_plan.md)
- [quickstart.md](quickstart.md)
- [privacy_model.md](privacy_model.md)
- [input_formats.md](input_formats.md)

功能：

- [demo_assets.py](../cli/lake_skill/demo_assets.py)
- [bundle.py](../cli/lake_skill/bundle.py)
- [cli.py](../cli/lake_skill/cli.py)
- [doctor_checks.py](../cli/lake_skill/doctor_checks.py)
- [safety_notice.md](../skills/lake-skill/prompts/safety_notice.md)

示例素材：

- [examples/social_demo](../examples/social_demo)
- [examples/social_demo/social_assets](../examples/social_demo/social_assets)

## 8. 验收清单

公开材料：

- README 首屏能回答“这是什么、适合谁、怎么试、为什么可信”。
- 小红书有 12 个题目和 4 篇可发布样稿。
- 抖音有 8 条短视频脚本和 2 个录屏 Demo。
- 仓库公开材料不引用本地私有分析内容。
- 示例素材只使用合成数据。
- 公开文案不使用承诺型、操控型、依赖诱导型、临床判断型表述。

命令验收：

```powershell
conda activate skills
python -m lake_skill.cli --help
python -m lake_skill.cli demo --out examples/social_demo
python -m lake_skill.cli doctor --messages examples/social_demo/work/messages.redacted.jsonl --sessions examples/social_demo/work/sessions.redacted.jsonl --out examples/social_demo/work
python -m lake_skill.cli bundle --source examples/social_demo --out examples/social_demo/upload_bundle
python -m lake_skill.cli audit examples/social_demo
python -m lake_skill.cli report-lint examples/social_demo
python -m lake_skill.cli check-leaks examples/social_demo
python tools/check.py --quick
python tools/check_expected_output.py
```

注意：`tools/check_expected_output.py` 依赖 `examples/model_outputs/` 下的实际模型输出样例。若仓库只保留 README，需要先补齐可公开的样例输出再运行完整场景检查。

## 9. 后续复盘问题

- GitHub 安装转化是否卡在依赖安装、Skill 安装、还是示例理解。
- 小红书收藏率最高的是隐私安全、关系纠偏，还是工具教程。
- 抖音完播率最高的是行动卡演示、doctor 三档解释，还是本地脱敏流程。
- 是否需要把 `demo` 输出进一步拆成“小红书长图包”和“抖音录屏包”。
- 是否需要为商业服务单独建立合规模板和客户交付边界。
