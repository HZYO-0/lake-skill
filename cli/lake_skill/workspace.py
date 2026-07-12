"""Per-contact workspace isolation and incremental coverage state."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path


def contact_workspace(root: Path, display_name: str) -> Path:
    normalized = display_name.strip() or "unknown-contact"
    safe = re.sub(r"[^\w\-\u4e00-\u9fff]+", "-", normalized, flags=re.UNICODE).strip("-")
    safe = safe[:48] or "contact"
    digest = hashlib.sha256(normalized.casefold().encode("utf-8")).hexdigest()[:10]
    return root / "contacts" / f"{safe}__{digest}"


def source_fingerprint(path: Path) -> dict:
    resolved = path.resolve()
    stat = resolved.stat()
    return {
        "path_hash": hashlib.sha256(str(resolved).encode("utf-8")).hexdigest(),
        "size": stat.st_size,
        "modified_ns": stat.st_mtime_ns,
    }


def write_workspace_state(
    workspace: Path,
    *,
    source: Path,
    mode: str,
    privacy_mode: str,
    message_count: int | None = None,
) -> None:
    state = {
        "schema_version": "0.12.0",
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "source": source_fingerprint(source),
        "analysis_mode": mode,
        "privacy_mode": privacy_mode,
        "message_count": message_count,
        "incremental_policy": "same contact reuses this directory; changed source coverage is recomputed",
    }
    (workspace / "workspace_state.json").write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def resolve_text_route(text: str) -> str:
    normalized = text.strip().lower()
    aliases = {
        "/急": "quick",
        "/深度": "deep",
        "/画像": "profile",
        "/复盘": "review",
        "/更新": "update",
        "/改写": "rewrite",
    }
    return aliases.get(normalized, "unknown")
