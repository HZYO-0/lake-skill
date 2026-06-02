"""Base adapter interface."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Generator, Optional

from ..schema import Message


class BaseAdapter(ABC):
    """Base adapter for converting various input formats to standard messages."""

    def __init__(self, warnings_path: Optional[Path] = None) -> None:
        """Initialize adapter with optional warnings output path."""
        self.warnings_path = warnings_path
        self.warnings: list[dict[str, Any]] = []

    @abstractmethod
    def read(self, file_path: Path, **kwargs: Any) -> Generator[Message, None, None]:
        """Read messages from file.

        Args:
            file_path: Path to input file
            **kwargs: Additional adapter-specific arguments

        Yields:
            Message objects
        """
        pass

    def add_warning(self, line_num: int, message: str, raw_line: str = "") -> None:
        """Add a parse warning."""
        warning = {
            "line": line_num,
            "message": message,
            "raw_line": raw_line[:500] if raw_line else "",
        }
        self.warnings.append(warning)

    def save_warnings(self) -> None:
        """Save warnings to file if path is set."""
        if self.warnings_path and self.warnings:
            import json

            with open(self.warnings_path, "w", encoding="utf-8") as f:
                for warning in self.warnings:
                    f.write(json.dumps(warning, ensure_ascii=False) + "\n")

    def process(self, file_path: Path, output_path: Path, **kwargs: Any) -> int:
        """Process input file and write to output.

        Args:
            file_path: Path to input file
            output_path: Path to output JSONL file
            **kwargs: Additional adapter-specific arguments

        Returns:
            Number of messages processed
        """

        count = 0
        with open(output_path, "w", encoding="utf-8") as f:
            for message in self.read(file_path, **kwargs):
                f.write(message.model_dump_json() + "\n")
                count += 1

        self.save_warnings()
        return count
