"""Validate BondLens prompts files exist and have correct structure."""

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SKILL_ROOT = PROJECT_ROOT / "skills" / "bondlens"
PROMPTS_DIR = PROJECT_ROOT / "skill" / "prompts"

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
    assert "name: bondlens" in frontmatter
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
    """report_builder.md defines the 8-layer output structure."""
    content = (PROMPTS_DIR / "report_builder.md").read_text(encoding="utf-8")
    for layer in ["Layer 0", "Layer 1", "Layer 2", "Layer 3",
                   "Layer 4", "Layer 5", "Layer 6", "Layer 7"]:
        assert layer in content, f"{layer} not found in report_builder.md"


def test_correction_handler_has_json_format():
    """correction_handler.md defines JSON correction format."""
    content = (PROMPTS_DIR / "correction_handler.md").read_text(encoding="utf-8")
    assert "scene" in content
    assert "wrong" in content
    assert "correct" in content


def test_merger_has_conflict_detection():
    """merger.md defines conflict detection flow."""
    content = (PROMPTS_DIR / "merger.md").read_text(encoding="utf-8")
    assert "冲突" in content or "conflict" in content.lower()
    assert "Patch" in content or "patch" in content


def test_coach_mode_has_multi_tone_templates():
    """coach_mode.md defines multi-tone reply templates."""
    content = (PROMPTS_DIR / "coach_mode.md").read_text(encoding="utf-8")
    assert "温和" in content
    assert "直接" in content
    assert "降压" in content
