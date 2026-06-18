# Model Outputs

This directory stores Skill outputs for structural validation.

Real private analysis outputs stay ignored by `.gitignore`. The committed
`*_output.md` files are synthetic fixtures only.

## How to use

1. Run the Skill with one of the test prompts from `examples/prompts/`
2. Save the full output as a `.md` file here
3. Run the structural checker:

```bash
# Check sparse input output (should NOT contain full analysis)
python tools/check_expected_output.py --scenario sparse examples/model_outputs/sparse_output.md

# Check representative input output (should contain 8-item analysis)
python tools/check_expected_output.py --scenario representative examples/model_outputs/representative_output.md

# Check CLI export output (should reference evidence/session IDs)
python tools/check_expected_output.py --scenario cli_export examples/model_outputs/cli_export_output.md
```

## Expected file naming

- `sparse_output.md` — Output from `examples/prompts/sparse_input.md`
- `representative_output.md` — Output from `examples/prompts/representative_input.md`
- `cli_export_output.md` — Output from `examples/prompts/cli_export_input.md`

## What the checker validates

| Scenario | Must contain | Must NOT contain |
|----------|-------------|-----------------|
| sparse | Data insufficiency statement | Full 8-item analysis, personality hypotheses |
| representative | Evidence IDs, confidence, alternatives | Certainty language, clinical diagnoses |
| cli_export | Evidence/session ID references | Requests for more raw data |

Do not add real chat analysis outputs here. Keep public fixtures synthetic.
