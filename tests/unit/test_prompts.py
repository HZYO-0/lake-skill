"""Validate LakeSkill prompts files exist and have correct structure."""

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SKILL_ROOT = PROJECT_ROOT / "skills" / "lake-skill"
PROMPTS_DIR = PROJECT_ROOT / "skills" / "lake-skill" / "prompts"

REQUIRED_PROMPTS = [
    "intake.md",
    "data_assessment.md",
    "communication_analyzer.md",
    "persona_analyzer.md",
    "attachment_analyzer.md",
    "interaction_analyzer.md",
    "report_builder.md",
    "merger.md",
    "correction_handler.md",
    "coach_mode.md",
    "action_brief_builder.md",
    "signal_weighting.md",
    "relationship_signal_extractor.md",
    "multi_factor_interpreter.md",
    "relationship_timeline_builder.md",
    "safety_notice.md",
]

REQUIRED_FRAMEWORKS = [
    "evidence_ladder.md",
    "big_five_communication_signals.md",
    "attachment_anxiety_avoidance.md",
    "relationship_communication_patterns.md",
    "forbidden_overclaims.md",
    "symbolic_mode_policy.md",
    "coaching_dialogue_framework.md",
]


def test_skill_md_exists():
    """SKILL.md exists at skill root."""
    skill_md = SKILL_ROOT / "SKILL.md"
    assert skill_md.exists(), f"SKILL.md not found at {skill_md}"


def test_skill_md_has_frontmatter():
    """SKILL.md has required frontmatter fields."""
    content = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert content.startswith("---")
    # Extract frontmatter
    parts = content.split("---", 2)
    assert len(parts) >= 3, "Frontmatter not properly closed"
    frontmatter = parts[1]
    assert "name: lake-skill" in frontmatter
    assert "version:" in frontmatter
    assert "user-invocable:" in frontmatter
    assert "allowed-tools:" in frontmatter


@pytest.mark.parametrize("filename", REQUIRED_PROMPTS)
def test_prompt_exists(filename: str):
    """Required prompt file exists."""
    path = PROMPTS_DIR / filename
    assert path.exists(), f"Missing prompt: {path}"


@pytest.mark.parametrize("filename", REQUIRED_PROMPTS)
def test_prompt_not_empty(filename: str):
    """Prompt file is not empty."""
    path = PROMPTS_DIR / filename
    content = path.read_text(encoding="utf-8").strip()
    assert len(content) > 50, f"Prompt {filename} is too short ({len(content)} chars)"


@pytest.mark.parametrize("filename", REQUIRED_FRAMEWORKS)
def test_framework_exists(filename: str):
    """Required framework file exists."""
    path = SKILL_ROOT / "references" / "frameworks" / filename
    assert path.exists(), f"Missing framework: {path}"


def test_report_builder_has_layer_structure():
    """report_builder.md defines the 9-layer output structure (Layer -1 through Layer 7)."""
    content = (PROMPTS_DIR / "report_builder.md").read_text(encoding="utf-8")
    for layer in ["Layer -1", "Layer 0", "Layer 1", "Layer 2", "Layer 3",
                   "Layer 4", "Layer 5", "Layer 6", "Layer 7"]:
        assert layer in content, f"{layer} not found in report_builder.md"


def test_no_stale_eight_layer_reference():
    """No prompt file references '8 层' (should be '9 层')."""
    for md_file in PROMPTS_DIR.glob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        assert "8 层分析" not in content, (
            f"{md_file.name} contains stale '8 层分析' reference (should be '9 层')"
        )


def test_skill_version_is_v010():
    """SKILL.md is bumped to the 0.10.0 reliability workflow."""
    content = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert 'version: "0.10.0"' in content
    assert "关系信号台账" in content
    assert "可靠性审计" in content


def test_no_stale_skill_prompts_path():
    """No prompt or SKILL.md references old 'skill/prompts/' path."""
    files_to_check = list(PROMPTS_DIR.glob("*.md"))
    files_to_check.append(SKILL_ROOT / "SKILL.md")
    for md_file in files_to_check:
        content = md_file.read_text(encoding="utf-8")
        assert "skill/prompts/" not in content, (
            f"{md_file.name} references stale path 'skill/prompts/'"
        )


def test_correction_handler_has_json_format():
    """correction_handler.md defines JSON correction format."""
    content = (PROMPTS_DIR / "correction_handler.md").read_text(encoding="utf-8")
    assert "场景" in content or "scene" in content
    assert "正确" in content or "correct" in content


def test_merger_has_conflict_detection():
    """merger.md defines conflict detection flow."""
    content = (PROMPTS_DIR / "merger.md").read_text(encoding="utf-8")
    assert "冲突" in content or "conflict" in content.lower()
    assert "Patch" in content or "patch" in content


def test_coach_mode_has_multi_tone_templates():
    """coach_mode.md defines multi-tone reply templates."""
    content = (PROMPTS_DIR / "coach_mode.md").read_text(encoding="utf-8")
    assert "直接" in content
    assert "降压" in content


def test_v010_reliability_prompts_define_required_artifacts():
    """0.10.0 prompts require ledger, contradiction ledger, and multi-factor interpretation."""
    signal_extractor = (PROMPTS_DIR / "relationship_signal_extractor.md").read_text(encoding="utf-8")
    weighting = (PROMPTS_DIR / "signal_weighting.md").read_text(encoding="utf-8")
    report_builder = (PROMPTS_DIR / "report_builder.md").read_text(encoding="utf-8")
    persona = (PROMPTS_DIR / "persona_analyzer.md").read_text(encoding="utf-8")

    assert "relationship_signal_ledger.jsonl" in signal_extractor
    assert "contradiction_ledger.md" in signal_extractor
    assert "T4 永远不能推翻 T1" in weighting
    assert "relationship_signal_audit.py" in report_builder
    assert "stable_trait" in persona
    assert "self_statement" in persona


def test_action_brief_has_degraded_mode():
    """Action brief must degrade when T1 evidence or reliability audit is missing."""
    content = (PROMPTS_DIR / "action_brief_builder.md").read_text(encoding="utf-8")
    assert "降级行动卡" in content
    assert "缺少 T1" in content
    assert "审计状态" in content


def test_safety_notice_defines_required_public_boundaries():
    """Safety notice prompt defines identity, consent, crisis, and minor-use boundaries."""
    content = (PROMPTS_DIR / "safety_notice.md").read_text(encoding="utf-8")

    assert "AI 身份与范围" in content
    assert "证据整理" in content
    assert "不扮演对方" in content
    assert "数据与同意" in content
    assert "有权处理" in content
    assert "合成数据" in content
    assert "风险与危机" in content
    assert "自伤" in content
    assert "伤害他人" in content
    assert "被威胁" in content
    assert "被跟踪" in content
    assert "现实支持系统" in content
    assert "当地紧急服务" in content
    assert "未成年人限制" in content
    assert "不面向未成年人" in content


def test_skill_and_report_builder_require_safety_notice():
    """Skill workflow and report builder require the safety notice before Layer -1."""
    skill_content = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    report_builder = (PROMPTS_DIR / "report_builder.md").read_text(encoding="utf-8")

    assert "prompts/safety_notice.md" in skill_content
    assert "使用边界与风险提示" in report_builder
    assert "覆盖声明后" in report_builder
    assert "Layer -1 前" in report_builder
    assert "不能被省略" in report_builder
    assert "低置信" in report_builder
