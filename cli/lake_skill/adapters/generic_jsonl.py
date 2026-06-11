"""Generic JSONL adapter."""

from pathlib import Path
from typing import Any, Generator

from ..jsonl_utils import read_jsonl
from ..schema import Message
from .base import BaseAdapter


class GenericJSONLAdapter(BaseAdapter):
    """Adapter for reading standard JSONL files."""

    def read(self, file_path: Path, **kwargs: Any) -> Generator[Message, None, None]:
        """Read messages from JSONL file.

        Args:
            file_path: Path to JSONL file

        Yields:
            Message objects
        """
        for line_num, data in enumerate(read_jsonl(file_path), 1):
            try:
                yield Message(**data)
            except Exception as e:
                self.add_warning(line_num, str(e), str(data))
                continue
