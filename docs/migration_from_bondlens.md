# Migrating From BondLens to LakeSkill

LakeSkill 湖镜 is the full rebrand and package migration of the former BondLens project.

This is a breaking migration. The old `bondlens` command, Python import path, and Skill install path are intentionally not kept as compatibility aliases.

## What Changed

| Area | Old | New |
|---|---|---|
| Brand | BondLens 关系镜 | LakeSkill 湖镜 |
| Skill name | `bondlens` | `lake-skill` |
| Skill path | `skills/bondlens/` | `skills/lake-skill/` |
| Python package | `bondlens` | `lake-skill` |
| Python import | `bondlens.*` | `lake_skill.*` |
| CLI command | `bondlens` | `lake-skill` |
| Intake files | `bondlens_intake.yaml`, `bondlens_intake.md` | `lakeskill_intake.yaml`, `lakeskill_intake.md` |
| Report files | `bondlens_report*.md` | `lakeskill_report*.md` |

## Install Again

```bash
npx skills add HZYO-0/lake-skill -y
```

For explicit Codex installs:

```bash
npx skills add --repo HZYO-0/lake-skill --path skills/lake-skill -y
```

## Update CLI Usage

Replace old commands:

```bash
bondlens init ./my_project
bondlens ingest --file input/chat.csv --type csv --out work/raw_messages.jsonl
```

with:

```bash
lake-skill init ./my_project
lake-skill ingest --file input/chat.csv --type csv --out work/raw_messages.jsonl
```

## Update Python Imports

Replace:

```python
from bondlens.schema import Message
from bondlens.privacy.redactor import create_redactor
```

with:

```python
from lake_skill.schema import Message
from lake_skill.privacy.redactor import create_redactor
```

## Update Generated Filenames

New intake files are named:

```text
lakeskill_intake.yaml
lakeskill_intake.md
```

New default report names are:

```text
lakeskill_report.md
lakeskill_report_*.md
```

Existing historical reports do not need to be rewritten unless you want a fully renamed archive.

## Notes

- `docs/archive/**` keeps historical material as-is.
- Real or historical chat evidence that mentions the old name should remain unchanged.
- If GitHub repository renaming has not happened yet, badge links and `npx skills add HZYO-0/lake-skill` will work only after the remote repository is renamed.
