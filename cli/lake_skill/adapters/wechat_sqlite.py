"""WeChat SQLite adapter."""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Generator, Optional

from ..errors import EncryptedDatabaseError
from ..schema import (
    Message,
    MessageType,
    Modality,
    ParseConfidence,
    QualityInfo,
    SenderRole,
    SourceInfo,
)
from .base import BaseAdapter
from .sqlite_inspector import inspect_sqlite_schema, generate_schema_map


class WeChatSQLiteAdapter(BaseAdapter):
    """Adapter for reading WeChat SQLite databases."""

    def __init__(
        self,
        warnings_path: Optional[Path] = None,
        schema_map: Optional[dict[str, Any]] = None,
        self_id: Optional[str] = None,
        target_id: Optional[str] = None,
        conversation_id: Optional[str] = None,
    ) -> None:
        """Initialize adapter.

        Args:
            warnings_path: Path to write warnings
            schema_map: Schema mapping configuration
            self_id: Self user ID
            target_id: Target user ID
            conversation_id: Conversation ID to filter
        """
        super().__init__(warnings_path)
        self.schema_map = schema_map
        self.self_id = self_id
        self.target_id = target_id
        self.conversation_id = conversation_id

    def _get_column_name(self, schema_map: dict[str, Any], field: str) -> Optional[str]:
        """Get column name from schema map."""
        columns = schema_map.get("columns", {})
        return columns.get(field)

    def _parse_timestamp(self, value: Any, unit: str = "seconds") -> Optional[datetime]:
        """Parse timestamp value."""
        if value is None:
            return None

        try:
            if isinstance(value, (int, float)):
                # Unix timestamp
                if unit == "milliseconds":
                    value = value / 1000
                return datetime.fromtimestamp(value)
            elif isinstance(value, str):
                # Try parsing string timestamp
                return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except Exception:
            return None
        return None

    def _determine_sender_role(
        self, sender_id: Optional[str], talker: Optional[str] = None
    ) -> SenderRole:
        """Determine sender role based on ID."""
        if not sender_id:
            return SenderRole.UNKNOWN

        if self.self_id and sender_id == self.self_id:
            return SenderRole.SELF
        if self.target_id and sender_id == self.target_id:
            return SenderRole.TARGET

        # If talker matches self_id, sender is target
        if self.self_id and talker == self.self_id:
            return SenderRole.TARGET
        if self.target_id and talker == self.target_id:
            return SenderRole.SELF

        return SenderRole.UNKNOWN

    def read(self, file_path: Path, **kwargs: Any) -> Generator[Message, None, None]:
        """Read messages from SQLite database.

        Args:
            file_path: Path to SQLite database

        Yields:
            Message objects

        Raises:
            EncryptedDatabaseError: If database is encrypted
        """
        # Inspect schema if no schema_map provided
        if not self.schema_map:
            inspection = inspect_sqlite_schema(file_path)
            if inspection.is_encrypted:
                raise EncryptedDatabaseError(str(file_path))
            if inspection.error:
                raise Exception(f"Error inspecting database: {inspection.error}")
            if not inspection.candidate_message_tables:
                raise Exception("No message tables found in database")

            # Use best candidate
            best_candidate = inspection.candidate_message_tables[0]
            self.schema_map = generate_schema_map(inspection, best_candidate.table)

        table_name = self.schema_map.get("table")
        if not table_name:
            raise Exception("No table specified in schema map")

        # Get column mappings
        timestamp_col = self._get_column_name(self.schema_map, "timestamp")
        sender_col = self._get_column_name(self.schema_map, "sender_id")
        text_col = self._get_column_name(self.schema_map, "text")
        msg_type_col = self._get_column_name(self.schema_map, "message_type")
        talker_col = self._get_column_name(self.schema_map, "conversation_id")

        if not timestamp_col or not text_col:
            raise Exception("Schema map must include timestamp and text columns")

        # Build query
        columns = [timestamp_col, text_col]
        if sender_col:
            columns.append(sender_col)
        if msg_type_col:
            columns.append(msg_type_col)
        if talker_col:
            columns.append(talker_col)

        query = f"SELECT {', '.join(columns)} FROM {table_name}"
        params = []

        # Filter by conversation if specified
        if self.conversation_id and talker_col:
            query += f" WHERE {talker_col} = ?"
            params.append(self.conversation_id)

        query += f" ORDER BY {timestamp_col}"

        # Execute query
        conn = sqlite3.connect(str(file_path))
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)

            for row_num, row in enumerate(cursor, 1):
                try:
                    # Extract values
                    timestamp_val = row[0]
                    text_val = row[1]
                    sender_val = row[2] if sender_col else None
                    talker_val = row[4] if talker_col else None

                    # Parse timestamp
                    timestamp = self._parse_timestamp(timestamp_val)
                    if not timestamp:
                        self.add_warning(row_num, f"Invalid timestamp: {timestamp_val}")
                        continue

                    # Determine sender role
                    sender_role = self._determine_sender_role(sender_val, talker_val)

                    # Create message
                    message = Message(
                        message_id=f"sqlite_{row_num}",
                        conversation_id=self.conversation_id or "default",
                        source_type="sqlite",
                        timestamp=timestamp,
                        sender_id=sender_val,
                        sender_role=sender_role,
                        message_type=MessageType.TEXT,
                        modality=Modality.TEXT,
                        text=str(text_val) if text_val else "",
                        raw_text=str(text_val) if text_val else "",
                        source=SourceInfo(
                            file=str(file_path),
                            table=table_name,
                            row_id=row_num,
                        ),
                        quality=QualityInfo(
                            parse_confidence=ParseConfidence.HIGH,
                            timestamp_confidence=ParseConfidence.HIGH,
                        ),
                    )
                    yield message

                except Exception as e:
                    self.add_warning(row_num, str(e))
                    continue
        finally:
            conn.close()
