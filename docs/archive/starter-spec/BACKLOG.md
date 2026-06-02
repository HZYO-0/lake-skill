# Backlog / GitHub Issues Seed

## Epic 1: Project skeleton

- [ ] Create repository structure.
- [ ] Add README, SECURITY, CONTRIBUTING, CODE_OF_CONDUCT.
- [ ] Add pyproject.toml.
- [ ] Add Makefile.
- [ ] Add config.default.yaml.
- [ ] Add strict .gitignore.

## Epic 2: Skill package

- [ ] Add skill/SKILL.md.
- [ ] Add agents/openai.yaml.
- [ ] Add framework references.
- [ ] Add KB templates.
- [ ] Add report templates.
- [ ] Add skill validation script.
- [ ] Add skill packaging workflow.

## Epic 3: CLI foundation

- [ ] Implement `wri init`.
- [ ] Implement config loader.
- [ ] Implement JSONL reader/writer.
- [ ] Implement schema validation.
- [ ] Implement logging and error model.

## Epic 4: Input adapters

- [ ] Generic JSONL adapter.
- [ ] Generic CSV adapter.
- [ ] WeChat CSV adapter.
- [ ] WeChat TXT adapter.
- [ ] WeChat HTML adapter.
- [ ] SQLite schema inspector.
- [ ] SQLite ingestion with schema_map.
- [ ] Voice transcript adapter.
- [ ] OCR transcript adapter.

## Epic 5: Privacy

- [ ] Implement privacy modes.
- [ ] Implement redactor.
- [ ] Implement deterministic hashing.
- [ ] Implement leak checker.
- [ ] Add privacy fixture scan to CI.

## Epic 6: Segmentation and evidence

- [ ] Sessionizer by time gap.
- [ ] Episode detector.
- [ ] Digest builder.
- [ ] Evidence indexer.
- [ ] Evidence quote length limiter.
- [ ] Evidence confidence downgrading for ASR/OCR.

## Epic 7: Knowledge base

- [ ] KB schema.
- [ ] KB init.
- [ ] KB patch.
- [ ] Update log.
- [ ] Confidence update rules.
- [ ] Counterevidence merge.

## Epic 8: Testing

- [ ] Unit tests for adapters.
- [ ] Unit tests for redaction.
- [ ] Unit tests for segmentation.
- [ ] Unit tests for evidence.
- [ ] Integration tests.
- [ ] Safety tests.
- [ ] Golden tests.
- [ ] Performance tests.

## Epic 9: Deployment

- [ ] Dockerfile.
- [ ] docker-compose.yml.
- [ ] CI workflow.
- [ ] Security workflow.
- [ ] Release workflow.
- [ ] Skill packaging workflow.

## Epic 10: Documentation

- [ ] Quickstart.
- [ ] Local deployment.
- [ ] ChatGPT Skill workflow.
- [ ] Input database policy.
- [ ] Media transcripts.
- [ ] Privacy model.
- [ ] Threat model.
- [ ] Output interpretation.
- [ ] Testing strategy.
- [ ] Release checklist.
