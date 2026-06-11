"""Package the canonical LakeSkill skill for multiple platforms.

Generates platform-specific installation packages in dist/:
  - chatgpt/       : SKILL.md + frameworks (for GPT Knowledge upload)
  - claude/        : .claude/skills/lake-skill/
  - codex/         : .codex/skills/lake-skill/
  - opencode/      : .opencode/skills/lake-skill/
  - openclaw/      : .openclaw/workspace/skills/lake-skill/
  - agents/        : .agents/skills/lake-skill/

Usage:
    python tools/package_skill.py
"""

import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DIST_DIR = PROJECT_ROOT / "dist"
SKILL_PACKAGE_DIR = PROJECT_ROOT / "skills" / "lake-skill"
FRAMEWORKS_DIR = SKILL_PACKAGE_DIR / "references" / "frameworks"

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
        try:
            shutil.rmtree(DIST_DIR)
        except PermissionError as exc:
            print(f"Warning: could not remove existing dist directory: {exc}", file=sys.stderr)
            print("Continuing and overwriting LakeSkill package outputs in place.", file=sys.stderr)
    DIST_DIR.mkdir(parents=True, exist_ok=True)


def copy_skill_package(out: Path) -> None:
    """Copy the installable LakeSkill skill package into a platform directory."""
    out.mkdir(parents=True)
    shutil.copy2(SKILL_PACKAGE_DIR / "SKILL.md", out / "SKILL.md")

    for resource in ("references", "assets", "agents"):
        src = SKILL_PACKAGE_DIR / resource
        if src.exists():
            shutil.copytree(src, out / resource, dirs_exist_ok=True)


def package_chatgpt() -> None:
    """Package for ChatGPT Custom GPT (flat structure for upload)."""
    out = DIST_DIR / "chatgpt"
    out.mkdir(exist_ok=True)

    shutil.copy2(SKILL_PACKAGE_DIR / "SKILL.md", out / "SKILL.md")

    fw_out = out / "frameworks"
    fw_out.mkdir(exist_ok=True)
    for fw in FRAMEWORKS:
        src = FRAMEWORKS_DIR / fw
        if src.exists():
            shutil.copy2(src, fw_out / fw)

    (out / "SETUP.md").write_text(
        "# ChatGPT Setup\n\n"
        "1. Open ChatGPT -> Create a GPT\n"
        "2. Paste `SKILL.md` content into **Instructions**\n"
        "3. Upload all files from `frameworks/` to **Knowledge**\n"
        "4. Start by pasting chat records or saying \"帮我分析一下我们的聊天记录\"\n\n"
        "## Test prompts\n\n"
        "- **Sparse test**: Paste 5-10 messages -> should say data insufficient\n"
        "- **Full test**: Paste 50+ messages from multiple sessions -> should produce a 9-layer report\n",
        encoding="utf-8",
    )
    print(f"  chatgpt/ ({len(list(out.rglob('*')))} files)")


def package_platform(platform: str, skill_subpath: str, install_hint: str) -> None:
    """Package for a platform with skills directory structure."""
    out = DIST_DIR / platform / skill_subpath
    copy_skill_package(out)

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

    if not (SKILL_PACKAGE_DIR / "SKILL.md").exists():
        print(f"Missing canonical skill package: {SKILL_PACKAGE_DIR}", file=sys.stderr)
        return 1

    clean_dist()
    package_chatgpt()
    package_platform(
        "claude",
        ".claude/skills/lake-skill",
        "cp -r dist/claude/.claude/ ./.claude/",
    )
    package_platform(
        "codex",
        ".codex/skills/lake-skill",
        "cp -r dist/codex/.codex/ ./.codex/",
    )
    package_platform(
        "opencode",
        ".opencode/skills/lake-skill",
        "cp -r dist/opencode/.opencode/ ./.opencode/",
    )
    package_platform(
        "openclaw",
        ".openclaw/workspace/skills/lake-skill",
        "cp -r dist/openclaw/.openclaw/ ~/.openclaw/",
    )
    package_platform(
        "agents",
        ".agents/skills/lake-skill",
        "cp -r dist/agents/.agents/ ./.agents/",
    )

    print(f"\nDone. Packages in {DIST_DIR}/")
    print("  chatgpt/  - Paste SKILL.md to Instructions, upload frameworks/ to Knowledge")
    print("  claude/   - Copy .claude/ to project root or ~/.claude/")
    print("  codex/    - Copy .codex/ to project root")
    print("  opencode/ - Copy .opencode/ to project root")
    print("  openclaw/ - Copy .openclaw/ to ~/.openclaw/")
    print("  agents/   - Copy .agents/ to project root")
    return 0


if __name__ == "__main__":
    sys.exit(main())
