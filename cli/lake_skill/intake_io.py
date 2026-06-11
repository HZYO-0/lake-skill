"""Intake card I/O utilities."""

from pathlib import Path

import yaml

from .schema import IntakeCard


def save_intake_yaml(card: IntakeCard, path: Path) -> None:
    """Serialize IntakeCard to YAML file."""
    data = card.model_dump(mode="json")
    # Convert datetime to ISO string for YAML serialization
    if "created_at" in data and data["created_at"] is not None:
        data["created_at"] = data["created_at"]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.dump(data, allow_unicode=True, default_flow_style=False), encoding="utf-8")


def save_intake_md(card: IntakeCard, path: Path) -> None:
    """Generate human-readable markdown summary of intake card."""
    content = generate_intake_md_content(card)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def generate_intake_md_content(card: IntakeCard) -> str:
    """Return markdown string for intake card summary."""
    created = card.created_at.strftime("%Y-%m-%d %H:%M") if card.created_at else "N/A"
    return f"""# LakeSkill Intake Card

**Generated**: {created}
**Version**: {card.version}

---

## 关系信息

| 字段 | 值 |
|------|-----|
| 关系类型 | {card.relationship_type} |
| 当前状态 | {card.status} |
| 你的称呼 | {card.self_name or '(未填写)'} |
| 对方称呼 | {card.target_name or '(未填写)'} |
| 时长 | {card.duration or '(未填写)'} |

## 分析配置

| 字段 | 值 |
|------|-----|
| 分析目标 | {card.goal or '(未填写)'} |
| 数据来源 | {card.data_source or '(未填写)'} |
| 隐私模式 | {card.privacy_mode} |
| 输出偏好 | {card.output_preference} |
| 工作模式 | {card.work_mode.value} |

## 典型场景

{card.scene_summary or '(未提供)'}

---

*本文件由 `lake-skill intake` 生成。上传至 LakeSkill Skill 可跳过 intake 收集轮次。*
"""


def load_intake_yaml(path: Path) -> IntakeCard:
    """Load and validate IntakeCard from YAML file."""
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return IntakeCard(**data)
