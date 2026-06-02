# Release Checklist

## Before tagging

- [ ] All tests pass.
- [ ] No real chat data in repository.
- [ ] No raw `.db`, `.csv`, `.jsonl`, `.txt`, `.html`, `.srt`, `.vtt`, audio, image, or video files outside approved synthetic fixtures.
- [ ] `cloud-safe` is the default privacy mode.
- [ ] README clearly states that project does not decrypt WeChat databases.
- [ ] README clearly states that output is not clinical diagnosis.
- [ ] README clearly states that manipulation tactics are forbidden.
- [ ] Symbolic mode is disabled by default.
- [ ] Skill `SKILL.md` frontmatter is valid.
- [ ] `skill.zip` builds successfully.
- [ ] `skill.zip` size is within upload limits.
- [ ] checksums generated.

## Commands

```bash
ruff check .
mypy cli
pytest -q
python tools/check_no_real_private_data.py tests examples docs
python tools/check_no_forbidden_network_calls.py cli skill
make package-skill
sha256sum dist/skill.zip > dist/checksums.txt
```

## Release artifacts

- [ ] `skill.zip`
- [ ] `checksums.txt`
- [ ] source tarball
- [ ] release notes
