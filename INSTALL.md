# 安装指南

## 一句话安装（让 Agent 自己装）

把下面这句话粘贴给 Claude Code、Codex 或 OpenCode：

```
请帮我安装 bondlens skill：从 https://github.com/HZYO-0/bondlens 克隆仓库，把 skill/ 目录下的 SKILL.md 和 references/frameworks/ 复制到对应平台的 skills 目录。
```

---

## 手动安装

### Claude Code

```bash
# 项目内安装（推荐）
mkdir -p .claude/skills/bondlens/references/frameworks
cp skill/SKILL.md .claude/skills/bondlens/
cp skill/references/frameworks/*.md .claude/skills/bondlens/references/frameworks/

# 或全局安装
mkdir -p ~/.claude/skills/bondlens/references/frameworks
cp skill/SKILL.md ~/.claude/skills/bondlens/
cp skill/references/frameworks/*.md ~/.claude/skills/bondlens/references/frameworks/
```

### Codex

```bash
mkdir -p .codex/skills/bondlens/references/frameworks
cp skill/SKILL.md .codex/skills/bondlens/
cp skill/references/frameworks/*.md .codex/skills/bondlens/references/frameworks/
```

### OpenCode

```bash
# OpenCode 支持多个发现路径，任选其一
mkdir -p .opencode/skills/bondlens/references/frameworks
cp skill/SKILL.md .opencode/skills/bondlens/
cp skill/references/frameworks/*.md .opencode/skills/bondlens/references/frameworks/
```

### OpenClaw

```bash
mkdir -p ~/.openclaw/workspace/skills/bondlens/references/frameworks
cp skill/SKILL.md ~/.openclaw/workspace/skills/bondlens/
cp skill/references/frameworks/*.md ~/.openclaw/workspace/skills/bondlens/references/frameworks/
```

### ChatGPT Custom GPT

1. 打开 ChatGPT → Create a GPT
2. 把 `skill/SKILL.md` 全部内容粘贴到 **Instructions**
3. 把 `skill/references/frameworks/` 下 7 个 `.md` 文件上传到 **Knowledge**
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
