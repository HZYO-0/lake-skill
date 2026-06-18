"""Upload bundle utilities for LakeSkill local preprocessing artifacts."""

from __future__ import annotations

import shutil
from pathlib import Path


DEFAULT_BUNDLE_FILES = [
    "digest.redacted.md",
    "sessions.redacted.jsonl",
    "evidence.redacted.jsonl",
    "lakeskill_intake.yaml",
    "lakeskill_intake.md",
    "conversations.jsonl",
]


def create_upload_readme(copied_files: list[str]) -> str:
    """Return the upload instructions for a prepared bundle."""
    file_list = "\n".join(f"- `{name}`" for name in copied_files)
    return f"""# LakeSkill Upload Bundle

本文件夹是上传给 LakeSkill Skill 的预处理材料。

## 可以上传

{file_list}

## 不要上传原始聊天记录

- 上传前确认材料已脱敏，并已经运行 `lake-skill check-leaks <bundle_dir>`。
- 不要上传原始 `.db`、未脱敏 `.csv/.txt/.jsonl`、截图或语音文件。
- 不要上传原始数据库、聊天截图、语音、身份证件、联系方式或定位信息。
- 不要上传未获授权的第三方隐私材料。
- 不要把本文件夹用于公开展示；公开展示请使用 `lake-skill demo` 生成的合成示例。

## 风险与未成年人提示

- 如材料涉及危机、自伤、伤害他人、被威胁、被跟踪或现实暴力风险，请停止上传，并优先联系现实支持系统、当地紧急服务或合格专业帮助。
- 如材料涉及未成年人，不要用于亲密陪伴、关系推进或依赖型互动建议。

## 建议提示词

```text
使用 lake-skill，读取这些本地预处理产物。请先给湖镜行动卡，再给完整报告。
如果证据不足，请输出低置信度草案，不要做确定性判断。
```
"""


def bundle_upload_artifacts(source_dir: Path, output_dir: Path) -> list[str]:
    """Copy upload-ready artifacts from source_dir into output_dir."""
    if not source_dir.exists():
        raise FileNotFoundError(f"Source directory not found: {source_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)
    copied: list[str] = []
    for filename in DEFAULT_BUNDLE_FILES:
        src = source_dir / filename
        if not src.exists() and filename == "conversations.jsonl":
            src = source_dir / "work" / filename
        if not src.exists() and filename.startswith(("digest", "sessions", "evidence")):
            src = source_dir / "work" / filename
        if not src.exists():
            continue
        shutil.copy2(src, output_dir / filename)
        copied.append(filename)

    if not copied:
        raise FileNotFoundError(f"No LakeSkill upload artifacts found under: {source_dir}")

    (output_dir / "upload_readme.md").write_text(create_upload_readme(copied), encoding="utf-8")
    return copied
