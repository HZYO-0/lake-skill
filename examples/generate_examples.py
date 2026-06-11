"""Generate example outputs."""

import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lake_skill.adapters.generic_csv import GenericCSVAdapter
from lake_skill.privacy.redactor import create_redactor
from lake_skill.privacy.modes import PrivacyMode
from lake_skill.segmentation.sessionizer import segment_sessions
from lake_skill.evidence.indexer import index_evidence
from lake_skill.reports.digest import generate_digest
from lake_skill.schema import Message


def main():
    """Generate example outputs."""
    # Paths
    input_dir = Path("examples/synthetic_input")
    output_dir = Path("examples/synthetic_outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Read CSV
    print("Reading CSV...")
    csv_file = input_dir / "chat.csv"
    raw_messages_file = output_dir / "raw_messages.jsonl"

    adapter = GenericCSVAdapter(self_name="我", target_name="张三")
    count = adapter.process(csv_file, raw_messages_file)
    print(f"  Processed {count} messages")

    # Redact messages
    print("Redacting messages...")
    redactor = create_redactor(PrivacyMode.CLOUD_SAFE)

    with open(raw_messages_file, "r", encoding="utf-8") as f:
        messages = [json.loads(line) for line in f]

    redacted_messages = [redactor.redact_message(msg) for msg in messages]

    redacted_file = output_dir / "messages.redacted.jsonl"
    with open(redacted_file, "w", encoding="utf-8") as f:
        for msg in redacted_messages:
            f.write(json.dumps(msg, ensure_ascii=False) + "\n")
    print(f"  Redacted {len(redacted_messages)} messages")

    # Parse messages
    messages = [Message(**msg) for msg in redacted_messages]

    # Segment sessions
    print("Segmenting sessions...")
    sessions = segment_sessions(messages, time_gap_hours=6.0)
    print(f"  Created {len(sessions)} sessions")

    sessions_file = output_dir / "sessions.redacted.jsonl"
    with open(sessions_file, "w", encoding="utf-8") as f:
        for session in sessions:
            f.write(session.model_dump_json() + "\n")

    # Index evidence
    print("Indexing evidence...")
    evidence_list = index_evidence(messages, sessions)
    print(f"  Created {len(evidence_list)} evidence items")

    evidence_file = output_dir / "evidence.redacted.jsonl"
    with open(evidence_file, "w", encoding="utf-8") as f:
        for evidence in evidence_list:
            f.write(evidence.model_dump_json() + "\n")

    # Generate digest
    print("Generating digest...")
    digest_file = output_dir / "digest.redacted.md"
    generate_digest(messages, sessions, str(digest_file))
    print("  Generated digest")

    print("Done!")


if __name__ == "__main__":
    main()
