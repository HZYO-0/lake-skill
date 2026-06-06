# Zy-Tf BondLens Analysis

This folder contains a private example analysis for Zy and Tf. It is useful as a regression sample for BondLens v4.1 output quality.

## Current Version

| Item | Value |
|---|---|
| Framework | BondLens v4.1.0 |
| Data range | 2024-08-01 to 2026-06-05 |
| Source | WeChat chat records |
| Total messages | 223,197 |
| Sampling | Monthly 100-message samples plus full 2026-06 window |
| Evidence index | 44 records |

## v4.1 Files

| File | Purpose |
|---|---|
| `bondlens_report_zy_tf_v4.md` | Main report with Layer -1 relationship action card |
| `tf_persona_v4.md` | Tf 6-layer persona profile |
| `zy_persona_v4.md` | Zy 6-layer persona profile |
| `communication_patterns_v4.md` | Communication style and non-literal expression analysis |
| `interaction_patterns_v4.md` | Positive loops, negative loops, conflict paths, repair signals |
| `communication_playbook_v4.md` | Longer scenario playbook |
| `v3_vs_v4_comparison.md` | Comparison between label-style v3 and behavior-rule v4 |

## What Changed In v4.1

- The main report starts with a relationship action card.
- The action card gives current strategy, this week's actions, pitfalls, watch signals, and message drafts.
- Major claims cite evidence IDs from `evidence_index.jsonl`.
- Reports include coverage statements, confidence, counterevidence, and alternative explanations.
- `report_lint.py` and `evidence_audit.py` are used as quality checks.

## Review Notes

Current validation status should be checked with:

```bash
python scripts/report_lint.py
python scripts/evidence_audit.py
```

As of the latest review, risk words and layer coverage are clean, but the main report still has several conclusion-format warnings in nested profile sections. Treat those as report-polish items rather than safety failures.

## Older Files

The non-v4 files are retained as historical outputs for comparison. Prefer v4.1 files for current demos and documentation.
