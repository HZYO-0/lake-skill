"""Knowledge base patching."""

from datetime import datetime
from typing import Any, Optional

from ..schema import Evidence
from .schema import KBPatch, KBObservation, KnowledgeBase


# Theme -> opposing keywords for counterevidence detection (A4)
THEME_COUNTER_KEYWORDS: dict[str, list[str]] = {
    "情感表达": ["讨厌", "烦", "不想", "无所谓", "随便"],
    "关系压力": ["不想谈", "以后再说", "无所谓", "随便", "没想过"],
    "冲突": ["对不起", "抱歉", "和好", "原谅", "我错了"],
    "修复": ["生气", "讨厌", "烦", "不想和好", "没用"],
    "回避": ["想你", "见面", "聊聊", "谈谈", "在一起", "对不起", "抱歉", "和好"],
    "边界": ["可以", "好的", "没问题", "随便", "都行"],
    "日常分享": ["不想说", "没什么", "不知道", "随便"],
}


def create_kb_patch(
    kb: KnowledgeBase,
    new_evidence: list[Evidence],
    patch_id: Optional[str] = None,
) -> KBPatch:
    """Create a patch for the knowledge base.

    Args:
        kb: Current knowledge base
        new_evidence: New evidence to incorporate
        patch_id: Optional patch ID

    Returns:
        KB patch
    """
    if not patch_id:
        patch_id = f"patch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # Analyze new evidence
    new_observations: list[KBObservation] = []
    reinforced_observations: list[KBObservation] = []
    revised_observations: list[KBObservation] = []
    counterevidence: list[KBObservation] = []
    confidence_updates: list[dict[str, Any]] = []

    # Group evidence by theme
    theme_evidence: dict[str, list[Evidence]] = {}
    for evidence in new_evidence:
        for theme in evidence.theme:
            if theme not in theme_evidence:
                theme_evidence[theme] = []
            theme_evidence[theme].append(evidence)

    # Compare with existing observations
    existing_themes = set()
    for obs in kb.observations:
        for evidence_id in obs.evidence_ids:
            # Extract theme from observation ID
            if "obs_" in obs.id:
                theme = obs.id.split("_")[1]
                existing_themes.add(theme)

    # Process each theme
    for theme, evidences in theme_evidence.items():
        evidence_ids = [e.evidence_id for e in evidences]

        if theme in existing_themes:
            # Find existing observation
            existing_obs = None
            for obs in kb.observations:
                if f"obs_{theme}" in obs.id:
                    existing_obs = obs
                    break

            if existing_obs:
                # Check if this is counterevidence
                if _is_counterevidence(evidences, existing_obs):
                    counterevidence.append(KBObservation(
                        id=f"counter_{theme}_{len(counterevidence) + 1}",
                        type="counterevidence",
                        content=f"Counterevidence for {theme}",
                        evidence_ids=evidence_ids,
                        confidence="medium",
                    ))
                else:
                    # Reinforce existing observation
                    reinforced_observations.append(KBObservation(
                        id=existing_obs.id,
                        type="reinforced",
                        content=existing_obs.content,
                        evidence_ids=existing_obs.evidence_ids + evidence_ids,
                        confidence=_upgrade_confidence(existing_obs.confidence),
                    ))
        else:
            # New observation
            if len(evidence_ids) >= 2:
                new_observations.append(KBObservation(
                    id=f"obs_{theme}_{len(new_observations) + 1}",
                    type="new",
                    content=f"New pattern observed: {theme}",
                    evidence_ids=evidence_ids,
                    confidence="medium",
                ))

    # Generate summary
    summary = _generate_patch_summary(
        new_observations,
        reinforced_observations,
        revised_observations,
        counterevidence,
    )

    return KBPatch(
        patch_id=patch_id,
        new_observations=new_observations,
        reinforced_observations=reinforced_observations,
        revised_observations=revised_observations,
        counterevidence=counterevidence,
        confidence_updates=confidence_updates,
        summary=summary,
    )


def _is_counterevidence(evidences: list[Evidence], observation: KBObservation) -> bool:
    """Check if evidence is counterevidence to observation.

    Args:
        evidences: List of evidence
        observation: Existing observation

    Returns:
        True if counterevidence
    """
    # Extract theme from observation ID (e.g., "obs_冲突_1" -> "冲突")
    obs_theme = ""
    if "obs_" in observation.id:
        parts = observation.id.split("_")
        if len(parts) >= 2:
            obs_theme = parts[1]

    if not obs_theme:
        return False

    # Get counter keywords for the observation's theme
    counter_keywords = THEME_COUNTER_KEYWORDS.get(obs_theme, [])

    if not counter_keywords:
        return False

    # Check if any evidence contains counter keywords
    for evidence in evidences:
        if evidence.quote:
            if any(kw in evidence.quote for kw in counter_keywords):
                return True

    return False


def _upgrade_confidence(current: str) -> str:
    """Upgrade confidence level.

    Args:
        current: Current confidence level

    Returns:
        Upgraded confidence level
    """
    if current == "low":
        return "medium"
    elif current == "medium":
        return "high"
    return current


def _generate_patch_summary(
    new: list[KBObservation],
    reinforced: list[KBObservation],
    revised: list[KBObservation],
    counterevidence: list[KBObservation],
) -> str:
    """Generate patch summary.

    Args:
        new: New observations
        reinforced: Reinforced observations
        revised: Revised observations
        counterevidence: Counterevidence

    Returns:
        Summary string
    """
    parts = []
    if new:
        parts.append(f"{len(new)} new observations")
    if reinforced:
        parts.append(f"{len(reinforced)} reinforced observations")
    if revised:
        parts.append(f"{len(revised)} revised observations")
    if counterevidence:
        parts.append(f"{len(counterevidence)} counterevidence items")

    if not parts:
        return "No significant changes"

    return "KB patch includes: " + ", ".join(parts)


def save_kb_patch(patch: KBPatch, output_path: str) -> None:
    """Save KB patch to file.

    Args:
        patch: KB patch
        output_path: Output file path
    """
    lines = [
        "# Knowledge Base Patch",
        "",
        f"**Patch ID**: {patch.patch_id}",
        f"**Created**: {patch.created_at.isoformat()}",
        "",
        "## Summary",
        "",
        patch.summary,
        "",
    ]

    if patch.new_observations:
        lines.append("## New Observations")
        lines.append("")
        for obs in patch.new_observations:
            lines.append(f"### {obs.id}")
            lines.append(f"- **Type**: {obs.type}")
            lines.append(f"- **Content**: {obs.content}")
            lines.append(f"- **Evidence**: {', '.join(obs.evidence_ids)}")
            lines.append(f"- **Confidence**: {obs.confidence}")
            lines.append("")

    if patch.reinforced_observations:
        lines.append("## Reinforced Observations")
        lines.append("")
        for obs in patch.reinforced_observations:
            lines.append(f"### {obs.id}")
            lines.append(f"- **Content**: {obs.content}")
            lines.append(f"- **New Evidence**: {', '.join(obs.evidence_ids)}")
            lines.append(f"- **Confidence**: {obs.confidence}")
            lines.append("")

    if patch.counterevidence:
        lines.append("## Counterevidence")
        lines.append("")
        for obs in patch.counterevidence:
            lines.append(f"### {obs.id}")
            lines.append(f"- **Content**: {obs.content}")
            lines.append(f"- **Evidence**: {', '.join(obs.evidence_ids)}")
            lines.append("")

    if patch.unresolved_questions:
        lines.append("## Unresolved Questions")
        lines.append("")
        for question in patch.unresolved_questions:
            lines.append(f"- {question}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
