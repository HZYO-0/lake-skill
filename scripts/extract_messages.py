#!/usr/bin/env python3
"""
WeChat Chat Export Message Extractor
Extracts messages from specific time periods for relationship analysis.

Output is written to UTF-8 text files in the output/ directory.
"""

import json
import os
import sys
from datetime import datetime

# === Configuration ===
INPUT_FILE = os.environ.get("LAKE_SKILL_INPUT_FILE", "")
OUTPUT_DIR = os.environ.get("LAKE_SKILL_OUTPUT_DIR", "output")
SAMPLE_SIZE = 100  # messages per sample batch (unused in full mode)

if not INPUT_FILE:
    print("Error: Set LAKE_SKILL_INPUT_FILE environment variable to your WeChat export JSON path.")
    print("  Example: $env:LAKE_SKILL_INPUT_FILE='F:\\path\\to\\messages.json'")
    sys.exit(1)

# === Batches to extract ===
BATCHES = [
    # (name, start_date, end_date, include_all)
    ("batch1_2024_08", "2024-08-01", "2024-08-31", True),
    ("batch2_2024_09", "2024-09-01", "2024-09-30", True),
    ("batch3_2024_10", "2024-10-01", "2024-10-31", True),
    ("batch4_2024_11", "2024-11-01", "2024-11-30", True),
    ("batch5_2024_12", "2024-12-01", "2024-12-31", True),
    ("batch6_2025_01", "2025-01-01", "2025-01-31", True),
    ("batch7_2025_02", "2025-02-01", "2025-02-28", True),
    ("batch8_2025_03", "2025-03-01", "2025-03-31", True),
    ("batch9_2025_04", "2025-04-01", "2025-04-30", True),
    ("batch10_2025_05", "2025-05-01", "2025-05-31", True),
    ("batch11_2025_06", "2025-06-01", "2025-06-30", True),
    ("batch12_2025_07", "2025-07-01", "2025-07-31", True),
    ("batch13_2025_08", "2025-08-01", "2025-08-31", True),
    ("batch14_2025_09", "2025-09-01", "2025-09-30", True),
    ("batch15_2025_10", "2025-10-01", "2025-10-31", True),
    ("batch16_2025_11", "2025-11-01", "2025-11-30", True),
    ("batch17_2025_12", "2025-12-01", "2025-12-31", True),
    ("batch18_2026_01", "2026-01-01", "2026-01-31", True),
    ("batch19_2026_02", "2026-02-01", "2026-02-28", True),
    ("batch20_2026_03", "2026-03-01", "2026-03-31", True),
    ("batch21_2026_04", "2026-04-01", "2026-04-30", True),
    ("batch22_2026_05", "2026-05-01", "2026-05-31", True),
    ("batch23_2026_06", "2026-06-01", "2026-06-05", True),
]


def parse_timestamp(time_text):
    """Parse 'YYYY-MM-DD HH:MM:SS' to datetime."""
    return datetime.strptime(time_text, "%Y-%m-%d %H:%M:%S")


def format_message(msg):
    """Format a single message for output."""
    time_text = msg["createTimeText"][:16]  # YYYY-MM-DD HH:MM
    sender = "Zy" if msg.get("isSent", False) else "Tf"
    render_type = msg.get("renderType", "text")
    content = msg.get("content", "").strip()

    if not content and render_type in ("emoji", "image", "video", "voice", "file"):
        content = f"[{render_type}]"

    # Include quote info if present
    quote_content = ""
    if render_type == "quote" and msg.get("quoteContent"):
        quote_text = msg["quoteContent"][:80]
        quote_user = "self" if msg.get("quoteUsername", "") == msg.get("senderUsername", "") else "target"
        quote_content = f" (quoting {quote_user}: {quote_text})"

    return f"[{time_text}] {sender}: {content}{quote_content}"


def main():
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Loading messages.json ...", file=sys.stderr)
    with open(INPUT_FILE, encoding="utf-8") as f:
        data = json.load(f)

    messages = data["messages"]
    print(f"Total messages loaded: {len(messages)}", file=sys.stderr)

    # Build date index for fast slicing
    # Messages are already sorted by createTime ascending
    print("Building date index ...", file=sys.stderr)

    all_outputs = []

    for batch_name, start_str, end_str, include_all in BATCHES:
        start_dt = datetime.strptime(start_str, "%Y-%m-%d")
        end_dt = datetime.strptime(end_str, "%Y-%m-%d")
        # End of day
        end_dt = end_dt.replace(hour=23, minute=59, second=59)

        start_ts = start_dt.timestamp()
        end_ts = end_dt.timestamp()

        # Filter messages in range
        filtered = [
            m for m in messages
            if start_ts <= m["createTime"] <= end_ts
        ]

        total_in_range = len(filtered)

        # Build output
        lines = []
        lines.append("=" * 80)
        lines.append(f"BATCH: {batch_name}")
        lines.append(f"DATE RANGE: {start_str} to {end_str}")
        lines.append(f"TOTAL MESSAGES IN RANGE: {total_in_range}")
        lines.append(f"OUTPUT: {'ALL MESSAGES' if include_all else f'SAMPLE ({SAMPLE_SIZE} messages)'}")
        lines.append("=" * 80)
        lines.append("")

        if include_all:
            # Include every message
            selected = filtered
        else:
            # Smart sampling: take evenly distributed messages
            if total_in_range <= SAMPLE_SIZE:
                selected = filtered
            else:
                step = total_in_range / SAMPLE_SIZE
                indices = [int(i * step) for i in range(SAMPLE_SIZE)]
                selected = [filtered[i] for i in indices]

        for msg in selected:
            lines.append(format_message(msg))

        lines.append("")
        lines.append(f"--- END OF BATCH {batch_name} ---")
        lines.append("")

        batch_text = "\n".join(lines)
        all_outputs.append(batch_text)

        # Write individual batch file
        batch_path = os.path.join(OUTPUT_DIR, f"{batch_name}.txt")
        with open(batch_path, "w", encoding="utf-8") as f:
            f.write(batch_text)

        print(f"  {batch_name}: {total_in_range} total, {len(selected)} output", file=sys.stderr)

    # Write combined output
    combined_path = os.path.join(OUTPUT_DIR, "all_batches_combined.txt")
    with open(combined_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(all_outputs))

    # Write a summary
    summary_path = os.path.join(OUTPUT_DIR, "extraction_summary.txt")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("WECHAT CHAT EXTRACTION SUMMARY\n")
        f.write(f"Source: {os.path.basename(INPUT_FILE)}\n")
        f.write(f"Total messages: {len(messages)}\n")
        f.write(f"Date range: {messages[0]['createTimeText']} to {messages[-1]['createTimeText']}\n")
        f.write(f"Extraction date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Output directory: {OUTPUT_DIR}\n")
        f.write("\nBATCH DETAILS:\n")
        f.write("-" * 60 + "\n")

        for batch_name, start_str, end_str, include_all in BATCHES:
            start_dt = datetime.strptime(start_str, "%Y-%m-%d")
            end_dt = datetime.strptime(end_str + " 23:59:59", "%Y-%m-%d %H:%M:%S")
            start_ts = start_dt.timestamp()
            end_ts = end_dt.timestamp()
            total = sum(1 for m in messages if start_ts <= m["createTime"] <= end_ts)
            mode = "ALL" if include_all else f"SAMPLE({SAMPLE_SIZE})"
            f.write(f"  {batch_name}: {total:>6} msgs ({start_str} to {end_str}) [{mode}]\n")

    print("\nDone!", file=sys.stderr)
    print(f"Output directory: {OUTPUT_DIR}", file=sys.stderr)
    print(f"Combined file: {combined_path}", file=sys.stderr)
    print(f"Summary file: {summary_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
