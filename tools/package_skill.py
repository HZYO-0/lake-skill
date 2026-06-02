"""Package skill for multiple platforms from canonical SKILL.md.

Generates platform-specific installation packages in dist/:
  - chatgpt/       : SKILL.md + frameworks (for GPT Knowledge upload)
  - claude/        : .claude/skills/bondlens/
  - codex/         : .codex/skills/bondlens/
  - opencode/      : .opencode/skills/bondlens/
  - openclaw/      : .openclaw/workspace/skills/bondlens/
  - agents/        : .agents/skills/bondlens/

Usage:
    python tools/package_skill.py
"""

import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = PROJECT_ROOT / "skill"
DIST_DIR = PROJECT_ROOT / "dist"

FRAMEWORKS = [
    "evidence_ladder.md",
    "big_five_communication_signals.md",
    "attachment_anxiety_avoidance.md",
    "relationship_communication_patterns.md",
    "forbidden_overclaims.md",
    "symbolic_mode_policy.md",
    "coaching_dialogue_framework.md",
]


def clean_dist() -> None:
    """Remove existing dist directory."""
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True)


def package_chatgpt() -> None:
    """Package for ChatGPT Custom GPT (flat structure for upload)."""
    out = DIST_DIR / "chatgpt"
    out.mkdir()

    shutil.copy2(SKILL_DIR / "SKILL.md", out / "SKILL.md")

    fw_out = out / "frameworks"
    fw_out.mkdir()
    for fw in FRAMEWORKS:
        src = SKILL_DIR / "references" / "frameworks" / fw
        if src.exists():
            shutil.copy2(src, fw_out / fw)

    (out / "SETUP.md").write_text(
        "# ChatGPT Setup\n\n"
        "1. Open ChatGPT → Create a GPT\n"
        "2. Paste `SKILL.md` content into **Instructions**\n"
        "3. Upload all files from `frameworks/` to **Knowledge**\n"
        "4. Start by pasting chat records or saying \"帮我分析一下我们的聊天记录\"\n\n"
        "## Test prompts\n\n"
        "- **Sparse test**: Paste 5-10 messages → should say data insufficient\n"
        "- **Full test**: Paste 50+ messages from multiple sessions → should produce 8-item analysis\n",
        encoding="utf-8",
    )
    print(f"  chatgpt/ ({len(list(out.rglob('*')))} files)")


def package_platform(platform: str, skill_subpath: str, install_hint: str) -> None:
    """Package for a platform with skills directory structure."""
    out = DIST_DIR / platform / skill_subpath
    out.mkdir(parents=True)

    shutil.copy2(SKILL_DIR / "SKILL.md", out / "SKILL.md")

    fw_out = out / "references" / "frameworks"
    fw_out.mkdir(parents=True)
    for fw in FRAMEWORKS:
        src = SKILL_DIR / "references" / "frameworks" / fw
        if src.exists():
            shutil.copy2(src, fw_out / fw)

    kb_src = SKILL_DIR / "assets" / "kb_template"
    if kb_src.exists():
        kb_out = out / "assets" / "kb_template"
        shutil.copytree(kb_src, kb_out)

    # Generate INSTALL.txt
    (DIST_DIR / platform / "INSTALL.txt").write_text(
        f"{platform} Installation\n"
        f"{'=' * (len(platform) + 12)}\n\n"
        f"Copy the `{skill_subpath.split('/')[0]}/` directory to your project root:\n\n"
        f"  {install_hint}\n\n"
        f"Then start a conversation and say: \"帮我分析一下我们的聊天记录\"\n",
        encoding="utf-8",
    )
    print(f"  {platform}/ ({len(list(out.rglob('*')))} files)")


def main() -> int:
    print("Packaging skill for multiple platforms...\n")

    clean_dist()
    package_chatgpt()
    package_platform(
        "claude", ".claude/skills/bondlens",
        "cp -r dist/claude/.claude/ ./.claude/",
    )
    package_platform(
        "codex", ".codex/skills/bondlens",
        "cp -r dist/codex/.codex/ ./.codex/",
    )
    package_platform(
        "opencode", ".opencode/skills/bondlens",
        "cp -r dist/opencode/.opencode/ ./.opencode/",
    )
    package_platform(
        "openclaw", ".openclaw/workspace/skills/bondlens",
        "cp -r dist/openclaw/.openclaw/ ~/.openclaw/",
    )
    package_platform(
        "agents", ".agents/skills/bondlens",
        "cp -r dist/agents/.agents/ ./.agents/",
    )

    print(f"\nDone. Packages in {DIST_DIR}/")
    print("  chatgpt/  — Paste SKILL.md to Instructions, upload frameworks/ to Knowledge")
    print("  claude/   — Copy .claude/ to project root or ~/.claude/")
    print("  codex/    — Copy .codex/ to project root")
    print("  opencode/ — Copy .opencode/ to project root")
    print("  openclaw/ — Copy .openclaw/ to ~/.openclaw/")
    print("  agents/   — Copy .agents/ to project root")
    return 0


if __name__ == "__main__":
    sys.exit(main())
