"""SQLite schema inspector."""

import sqlite3
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional


@dataclass
class ColumnInfo:
    """Column information."""

    name: str
    type: str
    notnull: bool = False
    default: Any = None
    pk: bool = False


@dataclass
class TableInfo:
    """Table information."""

    name: str
    columns: list[ColumnInfo] = field(default_factory=list)


@dataclass
class CandidateTable:
    """Candidate message table."""

    table: str
    score: float
    reasons: list[str] = field(default_factory=list)


@dataclass
class SchemaInspection:
    """Schema inspection result."""

    tables: list[TableInfo] = field(default_factory=list)
    candidate_message_tables: list[CandidateTable] = field(default_factory=list)
    is_encrypted: bool = False
    error: Optional[str] = None


def inspect_sqlite_schema(db_path: Path) -> SchemaInspection:
    """Inspect SQLite database schema.

    Args:
        db_path: Path to SQLite database

    Returns:
        SchemaInspection with table information and candidates
    """
    result = SchemaInspection()

    conn = None
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        for (table_name,) in tables:
            # Get column info
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns_info = cursor.fetchall()

            columns = []
            for col in columns_info:
                col_info = ColumnInfo(
                    name=col[1],
                    type=col[2],
                    notnull=bool(col[3]),
                    default=col[4],
                    pk=bool(col[5]),
                )
                columns.append(col_info)

            table_info = TableInfo(name=table_name, columns=columns)
            result.tables.append(table_info)

            # Score table as potential message table
            score, reasons = _score_message_table(table_name, columns)
            if score > 0.3:
                result.candidate_message_tables.append(
                    CandidateTable(table=table_name, score=score, reasons=reasons)
                )

        # Sort candidates by score
        result.candidate_message_tables.sort(key=lambda x: x.score, reverse=True)

    except sqlite3.DatabaseError as e:
        error_msg = str(e).lower()
        if "encrypted" in error_msg or "not a database" in error_msg:
            result.is_encrypted = True
            result.error = "Database is encrypted or not readable"
        else:
            result.error = str(e)
    finally:
        if conn is not None:
            conn.close()

    return result


def _score_message_table(
    table_name: str, columns: list[ColumnInfo]
) -> tuple[float, list[str]]:
    """Score a table as potential message table.

    Args:
        table_name: Table name
        columns: List of column info

    Returns:
        Tuple of (score, reasons)
    """
    score = 0.0
    reasons = []

    # Check table name
    name_lower = table_name.lower()
    if "message" in name_lower or "msg" in name_lower or "chat" in name_lower:
        score += 0.3
        reasons.append(f"Table name '{table_name}' suggests messages")

    # Check for timestamp column
    timestamp_names = {"timestamp", "time", "date", "create_time", "created_at", "send_time"}
    has_timestamp = any(col.name.lower() in timestamp_names for col in columns)
    if has_timestamp:
        score += 0.25
        reasons.append("Has timestamp column")

    # Check for text/content column
    text_names = {"content", "text", "message", "msg", "body"}
    has_text = any(col.name.lower() in text_names for col in columns)
    if has_text:
        score += 0.25
        reasons.append("Has text/content column")

    # Check for sender column
    sender_names = {"sender", "talker", "from", "user", "username"}
    has_sender = any(col.name.lower() in sender_names for col in columns)
    if has_sender:
        score += 0.2
        reasons.append("Has sender column")

    return score, reasons


def generate_schema_map(inspection: SchemaInspection, table_name: str) -> dict[str, Any]:
    """Generate schema map for a table.

    Args:
        inspection: Schema inspection result
        table_name: Selected table name

    Returns:
        Schema map dictionary
    """
    table = next((t for t in inspection.tables if t.name == table_name), None)
    if not table:
        raise ValueError(f"Table '{table_name}' not found")

    # Try to map columns
    column_map = {}
    for col in table.columns:
        col_lower = col.name.lower()

        # Timestamp
        if col_lower in {"timestamp", "time", "date", "create_time", "created_at", "send_time"}:
            column_map["timestamp"] = col.name

        # Sender
        if col_lower in {"sender", "talker", "from", "user", "username"}:
            column_map["sender_id"] = col.name

        # Content
        if col_lower in {"content", "text", "message", "msg", "body"}:
            column_map["text"] = col.name

        # Message type
        if col_lower in {"type", "msg_type", "message_type"}:
            column_map["message_type"] = col.name

    return {
        "table": table_name,
        "columns": column_map,
    }
