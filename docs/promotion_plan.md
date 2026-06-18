# LakeSkill 湖镜 Promotion Plan

## Positioning

主定位：

```text
别让 AI 猜 TA 爱不爱你。让 LakeSkill 告诉你：聊天证据支持什么、不支持什么、下一步怎么做更稳。
```

LakeSkill should be presented as a calm relationship mirror for chat evidence, not as a partner simulator, persona replay tool, or generic advice bot.

Primary copy angle:

```text
AI 不该替你脑补关系答案。LakeSkill 只做一件事：把聊天证据整理成行动卡。
```

Secondary copy angles:

- For anxious readers: `TA 回得慢，不等于关系变冷。先看证据够不够。`
- For agent users: `给 Codex/Claude Code 装一个会降级判断的关系分析 Skill。`
- For privacy-sensitive users: `聊天记录很敏感。先本地脱敏、体检、打包，再决定上传什么。`

Primary CTA:

```text
GitHub 搜 LakeSkill 湖镜，先跑一次合成 demo。
```

Cold-start order:

1. GitHub / Skill install conversion.
2. Xiaohongshu Chinese discovery through scenario-based notes.
3. Douyin short-video amplification through screen recordings and concise narration.
4. Commercial exploration around privacy-first data preparation, local setup, report templates, and workflow support.

Do not promise relationship outcomes, label someone clinically, or offer pressure-based tactics. Public examples must use synthetic demo data only.

Reference surfaces:

- Xiaohongshu main product surface: <https://www.xiaohongshu.com/>
- Ocean Engine marketing product surface: <https://www.oceanengine.com/>
- CAC generative AI service rules: search the CAC site for `生成式人工智能服务管理暂行办法`.
- CAC AI anthropomorphic interaction rules: search the CAC site for `人工智能拟人化互动服务管理暂行办法`.

## GitHub Setup

Recommended GitHub About description:

```text
A calm relationship mirror for chat evidence: action cards, signal ledgers, reliability audits, and privacy-first local preprocessing.
```

Recommended repository topics:

```text
ai-skill
agent-skills
relationship-analysis
chat-analysis
privacy-first
evidence-based
codex
claude-code
wechat
communication-coaching
```

## Skill Directory Listing

Title:

```text
LakeSkill 湖镜 - A Calm Relationship Mirror
```

Short description:

```text
Turn relationship chat records into evidence-backed action cards, confidence-labeled interpretations, and ready-to-send messages.
```

Long description:

```text
LakeSkill is an agent Skill for analyzing intimate relationship chat records without pretending to be the other person. It reads pasted chats or locally preprocessed exports, builds a relationship signal ledger, checks evidence sufficiency, and produces a lake-mirror action card before the full report. Outputs include what to do this week, what not to overclaim, ready-to-send messages, confidence levels, counterevidence, alternative explanations, and safety boundaries. For sensitive or large datasets, the optional CLI can redact, segment, summarize, index evidence, check readiness, and bundle upload-ready artifacts locally before upload.
```

Key differentiators:

- Lake-mirror action card first, long report second.
- Evidence ledger before conclusions.
- T1-T4 signal weighting and timeline-first interpretation.
- Reliability audit for overclaims and missing counterevidence.
- Privacy-first local preprocessing CLI.
- `intake` for fewer context-gathering turns.
- `doctor` for upload readiness: local observation / action card / full report.
- `demo` for synthetic public examples.
- Explicit refusal of manipulation, persona simulation, and medical or psychological judgement.

## README Copy Guidance

The README should sell trust before depth:

1. Lead with the emotional problem: AI can sound too certain when relationship evidence is weak.
2. Show the concrete output: a lake-mirror action card with evidence IDs and confidence.
3. Offer three paths: quick paste, install Skill, local preprocessing.
4. Move package metadata after the value story.
5. Keep safety and privacy boundaries visible, but avoid making the first screen feel legalistic.

## Xiaohongshu Matrix

Platform style: image-led note, long image, carousel, calm personal voice, concrete before/after examples. CTA should be soft: search `LakeSkill 湖镜` or `GitHub lake-skill`. Do not paste real private chats.

### 12 Titles

1. TA 回得慢，只能说明一件事：证据还不够
2. 我做了一个不会替你上头的聊天分析工具
3. 把聊天记录交给 AI 前，先做这 3 步
4. 一段聊天能不能支撑“关系变冷”的判断？
5. LakeSkill 湖镜：先给行动卡，再给长报告
6. 为什么聊天分析必须有“置信度”
7. 不要把一次短回复当作整段关系的答案
8. 用合成聊天演示：行动卡是怎么来的
9. 聊天记录太多？先做本地脱敏和数据体检
10. 我为什么不做“情绪依赖型”AI 工具
11. 关系分析里，最重要的不是结论，是反证
12. 一个适合 Codex/Claude Code 的关系聊天 Skill

### Four Ready-To-Post Notes

#### Note 1: TA 回得慢，只能说明一件事：证据还不够

封面文案：

```text
TA 回得慢，是不在乎吗？
先别急着下结论。
```

正文：

```text
很多关系里的焦虑，来自我们把一个局部信号放大成整个关系的答案。

比如：
TA 今天回得很短。
TA 隔了两个小时才回。
TA 没有接住我的情绪。

这些都可以是信号，但它们通常只是低层级信号。它们更像天气，不一定等于气候。

我做 LakeSkill 湖镜时，第一条原则就是：先分证据层级，再给行动建议。

它会区分：
- 关系定义对话
- 情绪转折
- 反复出现的互动模式
- 日常回复速度和消息量

日常回复速度只能做背景，不能单独支撑强判断。

所以行动卡里更常见的建议不是“马上推进”或“马上撤退”，而是：
先降低压力，观察对方是否继续主动开启互动；如果要表达感受，只说一次，不连续追问。

LakeSkill 湖镜不是替你求一个答案，而是先帮你看清证据支持到哪里。

公开示例全部使用合成聊天记录。搜索：LakeSkill 湖镜 / GitHub lake-skill。
```

标签：

```text
#AI工具 #聊天分析 #亲密关系沟通 #隐私保护 #开源项目 #Codex
```

#### Note 2: 把聊天记录交给 AI 前，先做这 3 步

封面文案：

```text
聊天记录很敏感。
不要直接整包上传。
```

正文：

```text
我做 LakeSkill 湖镜时，把“本地预处理”放进了核心流程。

建议顺序是：

1. 本地导入
把 CSV / TXT / JSONL / 明文 SQLite / 语音转写整理成统一消息格式。

2. 本地脱敏
先把姓名、联系方式、地点、组织等信息处理掉，再考虑上传。

3. 数据体检
用 doctor 看数据能支持到什么程度：
- 只能局部观察
- 可出行动卡
- 可出完整报告

这一步很关键。消息很多，不代表证据就够；如果缺少关系定义、边界、冲突或修复信号，LakeSkill 应该降级，而不是强行给结论。

本地命令：

lake-skill redact ...
lake-skill doctor ...
lake-skill bundle ...

公开展示请用：
lake-skill demo --out examples/social_demo

不要把真实聊天记录拿来做公开内容。
```

标签：

```text
#隐私保护 #AI安全 #聊天记录 #本地处理 #开源工具
```

#### Note 3: 我做了一个不会替你上头的聊天分析工具

封面文案：

```text
它不扮演 TA。
它只解释证据。
```

正文：

```text
LakeSkill 湖镜不是陪聊工具，也不是把某个人模拟出来。

它做的事情更克制：

先把聊天记录变成证据；
再把证据放回时间线；
再看哪些判断有支持，哪些判断还不能说；
最后才给行动卡和消息草稿。

我希望它解决的是一种很具体的问题：

当你在关系里焦虑时，AI 不应该顺着你的情绪给一个很肯定的答案。

它应该告诉你：
- 这个判断的证据是什么
- 置信度是多少
- 有没有反证
- 还有什么替代解释
- 下一步怎么做风险更低

所以 LakeSkill 的第一屏是行动卡，不是长篇人格分析。

一句话：
别让 AI 猜 TA 爱不爱你。让 LakeSkill 告诉你：聊天证据支持什么、不支持什么、下一步怎么做更稳。
```

标签：

```text
#AI工具 #关系沟通 #开源 #ClaudeCode #Codex #情绪稳定
```

#### Note 4: 用合成聊天演示：行动卡是怎么来的

封面文案：

```text
行动卡不是凭感觉写的。
它要有证据 ID。
```

正文：

```text
我专门给 LakeSkill 做了一个公开安全的 demo 命令：

lake-skill demo --out examples/social_demo

它会生成：
- 合成聊天 CSV
- 脱敏消息 JSONL
- 会话切分
- 摘要
- 证据索引
- 湖镜行动卡 demo

这样做有两个原因。

第一，真实聊天记录不应该拿来公开展示。

第二，行动卡必须可追溯。

一个合格的行动建议，至少要说清楚：
- 什么情况下用
- 具体做什么
- 证据来自哪里
- 什么不能做
- 置信度到哪里为止

如果证据不足，LakeSkill 应该输出低置信度草案，而不是把话说满。

这就是我想做的“湖镜”：不是替你求答案，而是让水面先静下来。
```

标签：

```text
#开源项目 #AI工作流 #合成数据 #隐私安全 #LakeSkill
```

## Douyin Matrix

Format: 20-45 seconds, screen recording first, calm narration, one idea per video. Avoid private data. Use `lake-skill demo` output only.

### 8 Short Video Scripts

1. Title: 把聊天记录丢给 AI，最危险的是它太肯定
   Script: 3s hook “短回复不等于关系答案” -> show action card -> show evidence IDs -> CTA “GitHub 搜 LakeSkill 湖镜”.

2. Title: 我做了一个不会替你上头的关系分析工具
   Script: show README first screen -> narration “它不扮演 TA，只解释证据” -> show confidence/counterevidence fields.

3. Title: 聊天记录太多？先做数据体检再分析
   Script: show `lake-skill doctor` -> point to three tiers -> explain why high volume without T1 still needs downgrade.

4. Title: 公开演示不能用真实聊天，我用合成数据
   Script: run `lake-skill demo` -> show synthetic CSV -> show action card demo.

5. Title: 一张行动卡应该回答什么
   Script: zoom on current strategy, this-week actions, do-not-do list, ready-to-send message.

6. Title: AI 分析关系，为什么必须有反证
   Script: show report fields -> “证据、推断、置信度、反证、替代解释，一个都不能少”.

7. Title: 给 Codex/Claude Code 装一个关系分析 Skill
   Script: show install command -> show quick prompt -> show generated action card.

8. Title: 聊天记录上传前，先本地脱敏
   Script: show `redact`, `check-leaks`, `bundle` -> show upload bundle readme.

### Two Recording Demo Outlines

Detailed, publish-safe recording copy is generated by `lake-skill demo` under `examples/social_demo/social_assets/`.

#### Demo A: 35s GitHub-To-Action-Card

Scene list:

1. 0-3s: README headline and one-line positioning.
2. 3-8s: Terminal: `lake-skill demo --out examples/social_demo`.
3. 8-15s: Open `synthetic_chat.csv`.
4. 15-25s: Open `social_action_card_demo.md`; zoom on strategy and evidence.
5. 25-32s: Open README “为什么可信”.
6. 32-35s: CTA: `GitHub lake-skill` / `LakeSkill 湖镜`.

Narration:

```text
我做了一个关系聊天分析 Skill。它不扮演对方，也不替你确认对方心里怎么想。它先用合成聊天做演示，把证据整理成行动卡：当前局势、本周怎么做、哪些话不要说、下一句怎么发。公开演示只用合成数据，真实聊天先本地脱敏。
```

Generated script: `examples/social_demo/social_assets/douyin_recording_script.md`.

#### Demo B: 45s Privacy-First Pipeline

Scene list:

1. 0-4s: “聊天记录很敏感，不要直接整包上传.”
2. 4-12s: Show `redact` command.
3. 12-20s: Show `doctor` report with three tiers.
4. 20-28s: Show `bundle` output folder.
5. 28-38s: Show upload readme warning.
6. 38-45s: Show action card demo.

Narration:

```text
LakeSkill 的重点不是更会猜，而是更可检查。先本地脱敏，再做数据体检：数据只能局部观察、可出行动卡，还是可出完整报告。最后 bundle 只整理可上传材料，并提醒不要上传原始聊天。公开内容用 demo 合成数据，不用真实记录。
```

Generated checklist: `examples/social_demo/social_assets/recording_checklist.md`.

## Commercial Boundary

Safer commercial directions:

- Local preprocessing setup.
- Privacy and redaction workflow templates.
- Evidence-report templates.
- Team or personal workflow installation.
- Synthetic demo materials and education content.

Avoid for now:

- Public always-on emotional companion product.
- Relationship-outcome guarantees.
- Pressure, jealousy, withdrawal, or dependency tactics.
- Medical, mental-health, or minor-focused relationship services.

## Copy Guardrails

Use:

- evidence-backed action card
- confidence-labeled interpretation
- counterevidence and alternative explanations
- privacy-first local preprocessing
- not a persona simulator
- no outcome promises

Avoid:

- outcome certainty
- claims about hidden inner states
- clinical labels
- dependency-driven messaging
- real private chats as examples

## Content Priorities

1. Lead with the lake/mirror emotional hook, then narrow the claim to evidence-backed action.
2. Show a concrete lake-mirror action-card demo above the fold.
3. Compare against persona simulation without dismissing those projects.
4. Make trust mechanisms visible: ledger, weighting, audit, confidence, counterevidence.
5. Keep safety boundaries explicit and prominent.
6. Link to installation and quickstart before deep workflow details.
7. Never use real private analyses as promotional examples; use synthetic excerpts only.
