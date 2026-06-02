# Codex 安装说明

把以下内容粘贴给 Codex，让它自动安装 Skill。

---

```
请帮我安装 bondlens skill。

步骤：

1. 在当前项目根目录创建 .opencode/skills/bondlens/ 目录

2. 把 skill/SKILL.md 复制到 .opencode/skills/bondlens/SKILL.md

3. 把 skill/references/frameworks/ 下的所有 .md 文件复制到 .opencode/skills/bondlens/references/frameworks/

4. 完成后告诉我目录结构

这个 skill 用于分析亲密关系聊天记录，提供基于证据的沟通分析和教练指导。
```

---

## 手动安装

如果 AI 没有自动执行，可以手动操作：

```bash
mkdir -p .opencode/skills/bondlens/references/frameworks
cp skill/SKILL.md .opencode/skills/bondlens/
cp skill/references/frameworks/*.md .opencode/skills/bondlens/references/frameworks/
```

## 验证安装

```bash
# 检查文件是否存在
ls .opencode/skills/bondlens/SKILL.md
ls .opencode/skills/bondlens/references/frameworks/
```

## 使用方式

安装后直接在对话中粘贴聊天记录，或说"帮我分析一下我们的聊天记录"即可触发。
