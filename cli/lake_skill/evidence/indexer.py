"""Evidence indexer for WRI."""

from typing import Optional

from ..privacy.hashing import generate_evidence_id
from ..schema import Evidence, Message, Session


# Theme -> hypothesis ID mapping (A2: Hypothesis Linker)
THEME_HYPOTHESIS_MAP: dict[str, list[str]] = {
    "情感表达": ["attachment_anxiety_signals", "emotional_expressiveness"],
    "关系压力": ["relationship_pressure_pattern", "attachment_anxiety_signals"],
    "冲突": ["conflict_pattern", "emotional_reactivity"],
    "修复": ["repair_pattern", "secure_functioning_signals"],
    "回避": ["attachment_avoidance_signals", "conflict_avoidance"],
    "边界": ["boundary_expression", "secure_functioning_signals"],
    "日常分享": ["daily_connection_pattern", "social_engagement"],
}


# Theme -> alternative explanations mapping (A3: Alternative Explanation Generator)
THEME_ALTERNATIVE_EXPLANATIONS: dict[str, list[str]] = {
    "情感表达": [
        "可能是日常礼貌性表达",
        "可能受当下的情绪影响",
        "可能是社交习惯性用语",
    ],
    "关系压力": [
        "可能只是一般性讨论未来计划",
        "可能受外部因素影响（如家庭催促）",
        "可能是试探性表达而非明确要求",
    ],
    "冲突": [
        "可能是一次性情绪反应",
        "可能与外部压力有关（如工作、生活）",
        "可能是沟通方式差异而非真正的冲突",
    ],
    "修复": [
        "可能是社交礼貌而非真正的修复意图",
        "可能只是暂时的情绪缓解",
        "可能是为了避免进一步冲突",
    ],
    "回避": [
        "可能当时确实在忙",
        "可能表达能力有限，需要时间思考",
        "可能是话题本身的敏感性导致的自然反应",
    ],
    "边界": [
        "可能是暂时的情绪状态",
        "可能是对特定情境的反应而非普遍模式",
        "可能只是表达个人偏好而非真正的边界",
    ],
    "日常分享": [
        "可能只是维持联系的社交习惯",
        "可能是寻找话题的自然方式",
        "可能反映日常生活状态而非特定情感",
    ],
}


def create_evidence(
    message: Message,
    session: Session,
    sequence: int,
    themes: Optional[list[str]] = None,
    supports: Optional[list[str]] = None,
    confidence: str = "medium",
    alternative_explanations: Optional[list[str]] = None,
) -> Evidence:
    """Create evidence from a message.

    Args:
        message: Source message
        session: Session containing the message
        sequence: Evidence sequence number
        themes: List of themes
        supports: List of supported hypotheses
        confidence: Confidence level
        alternative_explanations: List of alternative explanations

    Returns:
        Evidence object
    """
    # Generate evidence ID
    evidence_id = generate_evidence_id(message.timestamp, sequence)

    # Get quote (limit length)
    quote = message.text or ""
    if len(quote) > 280:
        quote = quote[:277] + "..."

    # Get redacted quote
    quote_redacted = message.text_redacted or quote
    if len(quote_redacted) > 280:
        quote_redacted = quote_redacted[:277] + "..."

    # Adjust confidence based on source quality
    if message.quality.asr_confidence and message.quality.asr_confidence < 0.75:
        confidence = "low"
    elif message.quality.ocr_confidence and message.quality.ocr_confidence < 0.80:
        confidence = "low"

    return Evidence(
        evidence_id=evidence_id,
        session_id=session.session_id,
        message_ids=[message.message_id],
        source_app=message.source_app,
        source_type=message.source_type,
        message_type=message.message_type.value,
        speaker=message.sender_role,
        quote=quote,
        quote_redacted=quote_redacted,
        asr_confidence=message.quality.asr_confidence,
        ocr_confidence=message.quality.ocr_confidence,
        theme=themes or [],
        supports=supports or [],
        confidence=confidence,
        alternative_explanations=alternative_explanations or [],
        created_at=message.timestamp,
    )


def index_evidence(
    messages: list[Message],
    sessions: list[Session],
) -> list[Evidence]:
    """Index evidence from messages and sessions.

    Args:
        messages: List of messages
        sessions: List of sessions

    Returns:
        List of evidence objects
    """
    evidence_list: list[Evidence] = []
    sequence = 0

    # Create message to session mapping
    message_to_session: dict[str, Session] = {}
    for session in sessions:
        for msg_id in session.message_ids:
            message_to_session[msg_id] = session

    # Process messages
    for message in messages:
        # Skip system messages
        if message.message_type.value == "system":
            continue

        # Skip empty messages
        if not message.text:
            continue

        # Get session
        session_opt = message_to_session.get(message.message_id)
        if not session_opt:
            continue
        session = session_opt

        # Increment sequence
        sequence += 1

        # Detect themes
        themes = detect_themes(message)

        # Collect hypothesis links from all detected themes
        supports: list[str] = []
        for theme in themes:
            supports.extend(THEME_HYPOTHESIS_MAP.get(theme, []))
        supports = list(set(supports))  # Deduplicate

        # Collect alternative explanations from all detected themes
        alternative_explanations: list[str] = []
        for theme in themes:
            alternative_explanations.extend(THEME_ALTERNATIVE_EXPLANATIONS.get(theme, []))
        alternative_explanations = list(set(alternative_explanations))  # Deduplicate

        # Create evidence
        evidence = create_evidence(
            message=message,
            session=session,
            sequence=sequence,
            themes=themes,
            supports=supports,
            alternative_explanations=alternative_explanations,
        )

        evidence_list.append(evidence)

    return evidence_list


def detect_themes(message: Message) -> list[str]:
    """Detect themes in a message.

    Args:
        message: Message object

    Returns:
        List of detected themes
    """
    if not message.text:
        return []

    themes: list[str] = []
    text = message.text

    # Theme patterns
    theme_patterns = {
        "情感表达": ["喜欢", "爱", "想你", "思念", "在乎"],
        "关系压力": ["关系", "在一起", "未来", "承诺", "结婚"],
        "冲突": ["生气", "讨厌", "烦", "吵架", "分手"],
        "修复": ["对不起", "抱歉", "原谅", "和好"],
        "回避": ["不知道", "不确定", "以后再说", "改天"],
        "边界": ["需要空间", "个人空间", "不要", "不喜欢"],
        "日常分享": ["今天", "昨天", "工作", "吃饭", "睡觉"],
    }

    for theme, keywords in theme_patterns.items():
        if any(kw in text for kw in keywords):
            themes.append(theme)

    return themes


def save_evidence_index(
    evidence_list: list[Evidence],
    output_path: str,
) -> None:
    """Save evidence index to file.

    Args:
        evidence_list: List of evidence objects
        output_path: Output file path
    """

    with open(output_path, "w", encoding="utf-8") as f:
        for evidence in evidence_list:
            f.write(evidence.model_dump_json() + "\n")
