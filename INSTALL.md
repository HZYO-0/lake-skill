# 安装指南

## 一行安装（推荐）

在 Claude Code / Codex / OpenCode 中说：

> 帮我安装这个 skill：https://github.com/HZYO-0/bondlens

或用 CLI 工具（支持 55+ runtime）：

```bash
npx skills add HZYO-0/bondlens
```

---

## 手动安装

### Claude Code

```bash
# 项目内安装（推荐）
mkdir -p .claude/skills/bondlens/references/frameworks
cp SKILL.md .claude/skills/bondlens/
cp references/frameworks/*.md .claude/skills/bondlens/references/frameworks/

# 或全局安装
mkdir -p ~/.claude/skills/bondlens/references/frameworks
cp SKILL.md ~/.claude/skills/bondlens/
cp references/frameworks/*.md ~/.claude/skills/bondlens/references/frameworks/
```

### Codex

```bash
mkdir -p .codex/skills/bondlens/references/frameworks
cp SKILL.md .codex/skills/bondlens/
cp references/frameworks/*.md .codex/skills/bondlens/references/frameworks/
```

### OpenCode

```bash
# OpenCode 支持多个发现路径，任选其一
mkdir -p .opencode/skills/bondlens/references/frameworks
cp SKILL.md .opencode/skills/bondlens/
cp references/frameworks/*.md .opencode/skills/bondlens/references/frameworks/
```

### OpenClaw

```bash
mkdir -p ~/.openclaw/workspace/skills/bondlens/references/frameworks
cp SKILL.md ~/.openclaw/workspace/skills/bondlens/
cp references/frameworks/*.md ~/.openclaw/workspace/skills/bondlens/references/frameworks/
```

### ChatGPT Custom GPT

1. 打开 ChatGPT → Create a GPT
2. 把 `SKILL.md` 全部内容粘贴到 **Instructions**
3. 把 `references/frameworks/` 下 7 个 `.md` 文件上传到 **Knowledge**
4. 开始对话

---

## 验证安装

安装后在对话中说：

```
帮我分析一下我们的聊天记录
```

如果 Skill 回复"为了让分析更准，我需要先确认几件事"，说明安装成功。

---

## 依赖（仅 CLI 预处理需要）

```bash
pip install -e ".[dev]"
```

CLI 是可选的，只在隐私敏感场景下需要。直接使用 Skill 不需要安装任何依赖。

---

## 平台路径汇总

| 平台 | 项目内路径 | 全局路径 |
|------|-----------|---------|
| Claude Code | `.claude/skills/bondlens/` | `~/.claude/skills/bondlens/` |
| Codex | `.codex/skills/bondlens/` | — |
| OpenCode | `.opencode/skills/bondlens/` | — |
| OpenClaw | — | `~/.openclaw/workspace/skills/bondlens/` |
| ChatGPT | 粘贴到 Instructions + 上传 Knowledge | — |
