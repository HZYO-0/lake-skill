"""Episode detection for WRI."""

import re
from typing import Optional

from ..schema import Message, Session


# Episode type patterns
EPISODE_PATTERNS = {
    "conflict": [
        re.compile(r"(生气|讨厌|烦|滚|分手|离婚|不想理你)", re.IGNORECASE),
        re.compile(r"(为什么总是|每次都是|你总是)", re.IGNORECASE),
        re.compile(r"(吵架|争论|冲突)", re.IGNORECASE),
    ],
    "repair": [
        re.compile(r"(对不起|抱歉|不好意思|我错了)", re.IGNORECASE),
        re.compile(r"(原谅|理解|体谅)", re.IGNORECASE),
        re.compile(r"(和好|修复|重新开始)", re.IGNORECASE),
    ],
    "ambiguous": [
        re.compile(r"(喜欢|爱|想你|思念)", re.IGNORECASE),
        re.compile(r"(关系|在一起|未来)", re.IGNORECASE),
        re.compile(r"(暧昧|试探|不确定)", re.IGNORECASE),
    ],
    "reassurance": [
        re.compile(r"(放心|相信|信任|安全感)", re.IGNORECASE),
        re.compile(r"(不会离开|一直在|陪伴)", re.IGNORECASE),
        re.compile(r"(承诺|保证|一定)", re.IGNORECASE),
    ],
    "relationship_pressure": [
        re.compile(r"(结婚|见父母|同居|未来)", re.IGNORECASE),
        re.compile(r"(承诺|责任|认真)", re.IGNORECASE),
        re.compile(r"(关系定义|我们是什么关系)", re.IGNORECASE),
    ],
    "coldness": [
        re.compile(r"(嗯|哦|好吧|随便)", re.IGNORECASE),
        re.compile(r"(忙|没时间|改天)", re.IGNORECASE),
        re.compile(r"(不想说|没什么好说的)", re.IGNORECASE),
    ],
    "reconnection": [
        re.compile(r"(好久不见|最近怎么样|还在吗)", re.IGNORECASE),
        re.compile(r"(想起|回忆|以前)", re.IGNORECASE),
        re.compile(r"(重新联系|复联)", re.IGNORECASE),
    ],
    "breakup": [
        re.compile(r"(分手|结束|分开|不合适)", re.IGNORECASE),
        re.compile(r"(不要联系|各自安好|祝你幸福)", re.IGNORECASE),
        re.compile(r"(删除|拉黑|不再联系)", re.IGNORECASE),
    ],
    "boundary": [
        re.compile(r"(需要空间|个人空间|边界)", re.IGNORECASE),
        re.compile(r"(不要这样|请尊重|我需要)", re.IGNORECASE),
        re.compile(r"(不舒服|不喜欢|不要)", re.IGNORECASE),
    ],
}


def detect_episodes(
    session: Session,
    messages: list[Message],
) -> list[str]:
    """Detect episode types in a session.

    Args:
        session: Session object
        messages: List of messages in the session

    Returns:
        List of detected episode types
    """
    if not messages:
        return []

    detected_episodes: set[str] = set()

    # Combine all message text
    all_text = " ".join(m.text or "" for m in messages)

    # Check each episode type
    for episode_type, patterns in EPISODE_PATTERNS.items():
        for pattern in patterns:
            if pattern.search(all_text):
                detected_episodes.add(episode_type)
                break

    return list(detected_episodes)


def detect_emotion(messages: list[Message]) -> Optional[str]:
    """Detect dominant emotion in messages.

    Args:
        messages: List of messages

    Returns:
        Dominant emotion string or None
    """
    if not messages:
        return None

    # Simple emotion detection based on keywords
    emotion_keywords = {
        "positive": ["开心", "高兴", "快乐", "幸福", "喜欢", "爱"],
        "negative": ["生气", "难过", "伤心", "失望", "烦", "讨厌"],
        "neutral": ["嗯", "哦", "好的", "知道了"],
        "anxious": ["担心", "害怕", "焦虑", "不安", "紧张"],
    }

    all_text = " ".join(m.text or "" for m in messages)

    emotion_scores = {}
    for emotion, keywords in emotion_keywords.items():
        score = sum(1 for kw in keywords if kw in all_text)
        if score > 0:
            emotion_scores[emotion] = score

    if not emotion_scores:
        return None

    return max(emotion_scores, key=lambda k: emotion_scores.get(k) or 0)


def assess_risk_level(session: Session, messages: list[Message]) -> Optional[str]:
    """Assess risk level of a session.

    Args:
        session: Session object
        messages: List of messages

    Returns:
        Risk level string (low, medium, high) or None
    """
    if not messages:
        return None

    risk_indicators = 0

    # Check for conflict indicators
    conflict_patterns = EPISODE_PATTERNS.get("conflict", [])
    all_text = " ".join(m.text or "" for m in messages)

    for pattern in conflict_patterns:
        if pattern.search(all_text):
            risk_indicators += 1

    # Check for breakup indicators
    breakup_patterns = EPISODE_PATTERNS.get("breakup", [])
    for pattern in breakup_patterns:
        if pattern.search(all_text):
            risk_indicators += 2

    # Check message frequency imbalance
    if session.self_count > 0 and session.target_count > 0:
        ratio = max(session.self_count, session.target_count) / min(session.self_count, session.target_count)
        if ratio > 3:
            risk_indicators += 1

    # Determine risk level
    if risk_indicators >= 3:
        return "high"
    elif risk_indicators >= 1:
        return "medium"
    else:
        return "low"
