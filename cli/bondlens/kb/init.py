"""Knowledge base initialization."""

from datetime import datetime
from pathlib import Path
from typing import Optional

from ..schema import Evidence, Message, Session
from .schema import KBMetadata, KBProfile, KnowledgeBase, KBObservation


def initialize_kb(
    messages: list[Message],
    sessions: list[Session],
    evidence_list: list[Evidence],
    output_dir: str,
) -> KnowledgeBase:
    """Initialize knowledge base from data.

    Args:
        messages: List of messages
        sessions: List of sessions
        evidence_list: List of evidence
        output_dir: Output directory path

    Returns:
        Initialized knowledge base
    """
    # Create metadata
    metadata = KBMetadata(
        version="1.0",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        message_count=len(messages),
        session_count=len(sessions),
        evidence_count=len(evidence_list),
    )

    # Create profile
    profile = _create_initial_profile(messages, sessions)

    # Create initial observations
    observations = _create_initial_observations(evidence_list, sessions)

    # Generate unresolved questions
    unresolved_questions = _generate_unresolved_questions(evidence_list, sessions)

    # Create knowledge base
    kb = KnowledgeBase(
        metadata=metadata,
        profile=profile,
        observations=observations,
        unresolved_questions=unresolved_questions,
    )

    # Save to files
    _save_kb_files(kb, output_dir)

    return kb


def _create_initial_profile(
    messages: list[Message],
    sessions: list[Session],
) -> KBProfile:
    """Create initial target profile.

    Args:
        messages: List of messages
        sessions: List of sessions

    Returns:
        Initial profile
    """
    # Analyze communication patterns
    target_messages = [m for m in messages if m.sender_role.value == "target"]
    [m for m in messages if m.sender_role.value == "self"]

    # Calculate average message length
    target_lengths = [len(m.text or "") for m in target_messages]
    avg_length = sum(target_lengths) / len(target_lengths) if target_lengths else 0

    # Determine communication style
    if avg_length > 100:
        style = "detailed"
    elif avg_length > 50:
        style = "moderate"
    else:
        style = "concise"

    return KBProfile(
        relationship_type="ambiguous",
        communication_style=style,
    )


def _create_initial_observations(
    evidence_list: list[Evidence],
    sessions: Optional[list[Session]] = None,
) -> list[KBObservation]:
    """Create initial observations from evidence.

    Args:
        evidence_list: List of evidence
        sessions: Optional list of sessions for context

    Returns:
        List of observations
    """
    observations: list[KBObservation] = []

    # Group evidence by theme
    theme_evidence: dict[str, list[Evidence]] = {}
    for evidence in evidence_list:
        for theme in evidence.theme:
            if theme not in theme_evidence:
                theme_evidence[theme] = []
            theme_evidence[theme].append(evidence)

    # Create observations for each theme
    for theme, evidences in theme_evidence.items():
        evidence_ids = [e.evidence_id for e in evidences]
        if len(evidence_ids) >= 2:  # Need at least 2 evidence for observation
            # Determine confidence based on evidence count
            confidence = "medium" if len(evidence_ids) >= 3 else "low"

            # Generate natural language observation content
            content = _generate_observation_content(theme, evidences)

            observation = KBObservation(
                id=f"obs_{theme}_{len(observations) + 1}",
                type="new",
                content=content,
                evidence_ids=evidence_ids,
                confidence=confidence,
            )
            observations.append(observation)

    return observations


# Theme-specific observation templates
THEME_OBSERVATION_TEMPLATES: dict[str, str] = {
    "情感表达": (
        "在{date_range}期间，{speaker}在{session_count}个会话中就'{theme}'主题"
        "呈现{pattern_desc}。共{count}条相关证据。置信度：{confidence}。"
    ),
    "关系压力": (
        "在{date_range}期间，{speaker}在{session_count}个会话中就'{theme}'主题"
        "呈现{pattern_desc}。共{count}条相关证据。置信度：{confidence}。"
    ),
    "冲突": (
        "在{date_range}期间，{speaker}在{session_count}个会话中就'{theme}'主题"
        "呈现{pattern_desc}。共{count}条相关证据。置信度：{confidence}。"
    ),
    "修复": (
        "在{date_range}期间，{speaker}在{session_count}个会话中就'{theme}'主题"
        "呈现{pattern_desc}。共{count}条相关证据。置信度：{confidence}。"
    ),
    "回避": (
        "在{date_range}期间，{speaker}在{session_count}个会话中就'{theme}'主题"
        "呈现{pattern_desc}。共{count}条相关证据。置信度：{confidence}。"
    ),
    "边界": (
        "在{date_range}期间，{speaker}在{session_count}个会话中就'{theme}'主题"
        "呈现{pattern_desc}。共{count}条相关证据。置信度：{confidence}。"
    ),
    "日常分享": (
        "在{date_range}期间，{speaker}在{session_count}个会话中就'{theme}'主题"
        "呈现{pattern_desc}。共{count}条相关证据。置信度：{confidence}。"
    ),
}

# Theme-specific pattern descriptions
THEME_PATTERN_DESCRIPTIONS: dict[str, dict[str, str]] = {
    "情感表达": {
        "default": "情感表达倾向，包括喜欢、爱意、思念等情感词汇的使用",
        "self": "主动表达情感的倾向",
        "target": "对情感表达的回应模式",
    },
    "关系压力": {
        "default": "对关系定义和未来走向的关注，包括承诺、在一起、未来等话题",
        "self": "主动提出关系话题的倾向",
        "target": "对关系话题的回应模式",
    },
    "冲突": {
        "default": "冲突信号，包括生气、烦躁、吵架等负面情绪表达",
        "self": "在冲突中的表达模式",
        "target": "在冲突中的回应模式",
    },
    "修复": {
        "default": "修复意图，包括道歉、原谅、和好等修复性表达",
        "self": "主动修复的倾向",
        "target": "对修复尝试的回应模式",
    },
    "回避": {
        "default": "回避信号，包括延迟回应、话题转移、不确定表达等",
        "self": "在敏感话题上的回避模式",
        "target": "在敏感话题上的回避模式",
    },
    "边界": {
        "default": "边界表达，包括需要空间、个人边界、拒绝等",
        "self": "表达个人边界的模式",
        "target": "对边界的回应模式",
    },
    "日常分享": {
        "default": "日常分享模式，包括工作、生活、饮食等日常话题",
        "self": "主动分享日常的倾向",
        "target": "对日常分享的回应模式",
    },
}


def _generate_observation_content(theme: str, evidences: list[Evidence]) -> str:
    """Generate natural language observation content.

    Args:
        theme: The theme name
        evidences: List of evidence items for this theme

    Returns:
        Natural language observation string
    """
    from collections import Counter

    # Count speakers
    speaker_counts = Counter(e.speaker.value for e in evidences)
    dominant_speaker = speaker_counts.most_common(1)[0][0] if speaker_counts else "unknown"

    # Get date range
    dates = [e.created_at for e in evidences if e.created_at]
    if dates:
        min_date = min(dates).strftime("%Y-%m-%d")
        max_date = max(dates).strftime("%Y-%m-%d")
        if min_date == max_date:
            date_range = min_date
        else:
            date_range = f"{min_date}至{max_date}"
    else:
        date_range = "未知时间"

    # Count unique sessions
    session_ids = set(e.session_id for e in evidences)
    session_count = len(session_ids)

    # Get pattern description
    pattern_desc = THEME_PATTERN_DESCRIPTIONS.get(
        theme, {"default": f"'{theme}'相关行为模式"}
    ).get(dominant_speaker, THEME_PATTERN_DESCRIPTIONS.get(theme, {}).get("default", f"'{theme}'相关行为模式"))

    # Determine confidence
    confidence = "中等" if len(evidences) >= 3 else "低"

    # Build speaker label
    speaker_label = {"self": "用户", "target": "对方", "other": "第三方"}.get(
        dominant_speaker, dominant_speaker
    )

    # Use template
    template = THEME_OBSERVATION_TEMPLATES.get(theme, THEME_OBSERVATION_TEMPLATES["日常分享"])
    content = template.format(
        date_range=date_range,
        speaker=speaker_label,
        session_count=session_count,
        theme=theme,
        pattern_desc=pattern_desc,
        count=len(evidences),
        confidence=confidence,
    )

    return content


def _generate_unresolved_questions(
    evidence_list: list[Evidence],
    sessions: Optional[list[Session]] = None,
) -> list[str]:
    """Generate unresolved questions from evidence and sessions.

    Args:
        evidence_list: List of evidence
        sessions: Optional list of sessions

    Returns:
        List of unresolved questions
    """
    questions: list[str] = []

    # Group evidence by theme
    theme_evidence: dict[str, list[Evidence]] = {}
    for evidence in evidence_list:
        for theme in evidence.theme:
            if theme not in theme_evidence:
                theme_evidence[theme] = []
            theme_evidence[theme].append(evidence)

    # Check for low-confidence themes (need more data)
    for theme, evidences in theme_evidence.items():
        if len(evidences) < 3:
            questions.append(
                f"关于'{theme}'主题的证据较少（仅{len(evidences)}条），"
                f"建议收集更多相关聊天记录以提高分析置信度。"
            )

    # Check for themes with alternative explanations (ambiguous)
    for theme, evidences in theme_evidence.items():
        has_alternatives = any(
            e.alternative_explanations and len(e.alternative_explanations) > 1
            for e in evidences
        )
        if has_alternatives:
            questions.append(
                f"关于'{theme}'主题存在多种可能的解释，"
                f"需要更多上下文来确定哪种解释更准确。"
            )

    # Check for high-risk sessions without repair
    if sessions:
        high_risk_sessions = [s for s in sessions if s.risk_level == "high"]
        repair_sessions = [
            s for s in sessions
            if s.episode_type and "repair" in s.episode_type
        ]
        if high_risk_sessions and not repair_sessions:
            questions.append(
                f"检测到{len(high_risk_sessions)}个高风险会话（可能涉及冲突），"
                f"但未检测到明确的修复会话。关系的冲突修复模式需要进一步观察。"
            )

    # Check for low-confidence evidence (ASR/OCR quality)
    low_confidence_count = sum(
        1 for e in evidence_list
        if e.confidence == "low"
    )
    if low_confidence_count > 0:
        questions.append(
            f"有{low_confidence_count}条证据的置信度较低（可能受语音转写或OCR质量影响），"
            f"这些证据的准确性需要人工确认。"
        )

    # Check for unanswered relationship pressure
    pressure_evidence = theme_evidence.get("关系压力", [])
    if pressure_evidence:
        # Check if there's corresponding avoidance
        avoidance_evidence = theme_evidence.get("回避", [])
        if len(pressure_evidence) > len(avoidance_evidence):
            questions.append(
                "检测到关系压力信号多于回避信号，"
                "对方对关系定义的态度需要进一步观察。"
            )

    return questions


def load_kb(kb_dir: str) -> KnowledgeBase:
    """Load existing knowledge base from directory.

    Args:
        kb_dir: Path to knowledge base directory

    Returns:
        Loaded knowledge base
    """
    import yaml

    kb_path = Path(kb_dir)
    if not kb_path.exists():
        raise FileNotFoundError(f"KB directory not found: {kb_path}")

    # Load metadata
    metadata_path = kb_path / "metadata.yaml"
    if metadata_path.exists():
        metadata_dict = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))
        metadata = KBMetadata(**metadata_dict)
    else:
        metadata = KBMetadata()

    # Load profile
    profile_path = kb_path / "target_profile.md"
    if profile_path.exists():
        profile = _parse_profile(profile_path.read_text(encoding="utf-8"))
    else:
        profile = KBProfile()

    # Load observations
    observations: list[KBObservation] = []
    obs_path = kb_path / "observations.jsonl"
    if obs_path.exists():
        for line in obs_path.read_text(encoding="utf-8").strip().split("\n"):
            if line.strip():
                observations.append(KBObservation.model_validate_json(line))

    # Load unresolved questions
    questions_path = kb_path / "unresolved_questions.md"
    unresolved_questions: list[str] = []
    if questions_path.exists():
        for line in questions_path.read_text(encoding="utf-8").split("\n"):
            line = line.strip()
            if line.startswith("- "):
                unresolved_questions.append(line[2:])

    return KnowledgeBase(
        metadata=metadata,
        profile=profile,
        observations=observations,
        unresolved_questions=unresolved_questions,
    )


def _parse_profile(content: str) -> KBProfile:
    """Parse profile from markdown content.

    Args:
        content: Markdown content

    Returns:
        KBProfile object
    """
    lines = content.split("\n")
    relationship_type = "ambiguous"
    communication_style = None
    emotional_patterns: list[str] = []
    attachment_signals: list[str] = []
    notes: list[str] = []

    current_section = None

    for line in lines:
        line = line.strip()
        if line.startswith("## "):
            current_section = line[3:].strip()
        elif line.startswith("- ") and current_section:
            item = line[2:].strip()
            if current_section == "Emotional Patterns":
                emotional_patterns.append(item)
            elif current_section == "Attachment Signals":
                attachment_signals.append(item)
            elif current_section == "Notes":
                notes.append(item)
        elif current_section == "Relationship Type" and line:
            relationship_type = line
        elif current_section == "Communication Style" and line and line != "Not determined":
            communication_style = line

    return KBProfile(
        relationship_type=relationship_type,
        communication_style=communication_style,
        emotional_patterns=emotional_patterns,
        attachment_signals=attachment_signals,
        notes=notes,
    )


def _save_kb_files(kb: KnowledgeBase, output_dir: str) -> None:
    """Save knowledge base to files.

    Args:
        kb: Knowledge base
        output_dir: Output directory
    """

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Save metadata
    with open(output_path / "metadata.yaml", "w", encoding="utf-8") as f:
        import yaml
        yaml.dump(kb.metadata.model_dump(), f, default_flow_style=False)

    # Save profile
    with open(output_path / "target_profile.md", "w", encoding="utf-8") as f:
        f.write(_format_profile(kb.profile))

    # Save observations
    with open(output_path / "observations.jsonl", "w", encoding="utf-8") as f:
        for obs in kb.observations:
            f.write(obs.model_dump_json() + "\n")

    # Save unresolved questions
    with open(output_path / "unresolved_questions.md", "w", encoding="utf-8") as f:
        f.write("# Unresolved Questions\n\n")
        if kb.unresolved_questions:
            for question in kb.unresolved_questions:
                f.write(f"- {question}\n")
        else:
            f.write("- No unresolved questions at this time.\n")

    # Save update log
    with open(output_path / "update_log.md", "w", encoding="utf-8") as f:
        f.write("# Update Log\n\n")
        f.write(f"- {datetime.now().isoformat()}: Initial knowledge base created\n")


def _format_profile(profile: KBProfile) -> str:
    """Format profile as markdown.

    Args:
        profile: Profile object

    Returns:
        Formatted markdown string
    """
    lines = [
        "# Target Profile",
        "",
        "## Relationship Type",
        f"{profile.relationship_type}",
        "",
        "## Communication Style",
        f"{profile.communication_style or 'Not determined'}",
        "",
    ]

    if profile.emotional_patterns:
        lines.append("## Emotional Patterns")
        for pattern in profile.emotional_patterns:
            lines.append(f"- {pattern}")
        lines.append("")

    if profile.attachment_signals:
        lines.append("## Attachment Signals")
        for signal in profile.attachment_signals:
            lines.append(f"- {signal}")
        lines.append("")

    if profile.notes:
        lines.append("## Notes")
        for note in profile.notes:
            lines.append(f"- {note}")

    return "\n".join(lines)
