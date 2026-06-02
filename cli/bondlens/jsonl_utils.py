"""JSONL streaming utilities."""

import json
from pathlib import Path
from typing import Any, Generator, Sequence

from pydantic import BaseModel


def read_jsonl(file_path: Path) -> Generator[dict[str, Any], None, None]:
    """Read JSONL file line by line."""
    with open(file_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON at line {line_num}: {e}") from e


def write_jsonl(file_path: Path, items: list[dict[str, Any]]) -> None:
    """Write items to JSONL file."""
    with open(file_path, "w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


def append_jsonl(file_path: Path, item: dict[str, Any]) -> None:
    """Append single item to JSONL file."""
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")


def read_jsonl_models(file_path: Path, model_class: type[BaseModel]) -> Generator[BaseModel, None, None]:
    """Read JSONL file and parse into Pydantic models."""
    for data in read_jsonl(file_path):
        yield model_class(**data)


def write_jsonl_models(file_path: Path, items: Sequence[BaseModel]) -> None:
    """Write Pydantic models to JSONL file."""
    write_jsonl(file_path, [item.model_dump(mode="json") for item in items])
