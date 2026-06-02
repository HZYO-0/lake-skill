# Development Plan

## 总体路线

开发按 10 个阶段推进。每阶段必须有交付物和验收标准。

## Phase 0: 需求冻结与边界定义

目标：明确产品边界、安全边界、默认部署模式。

交付物：

```text
docs/input_database_policy.md
docs/privacy_model.md
docs/threat_model.md
docs/output_interpretation.md
SECURITY.md
README.md
```

验收标准：

- README 明确写出默认模式：本地预处理 + ChatGPT Skill 分析。
- README 明确写出不解密、不越权、不诊断、不操控。
- 隐私模式定义清楚。
- 星座/塔罗默认禁用。

## Phase 1: Skill 骨架

目标：完成可上传的 Skill 目录。

交付物：

```text
skill/SKILL.md
skill/agents/openai.yaml
skill/references/frameworks/*.md
skill/assets/kb_template/*.md
```

验收标准：

- `SKILL.md` frontmatter 合法。
- description 覆盖：微信数据库、聊天导出、语音转文字、OCR、亲密关系、依恋/人格信号、沟通建议、KB 更新。
- Skill 明确禁止解密、诊断、操控。

## Phase 2: CLI 基础与标准 Schema

目标：搭建 CLI 和标准 JSONL 管线。

交付物：

```text
cli/wechat_relationship_insight/cli.py
cli/wechat_relationship_insight/schema.py
cli/wechat_relationship_insight/config.py
config.default.yaml
tests/unit/test_schema.py
```

验收标准：

- `wri --help` 正常。
- `wri init` 创建项目目录。
- 标准 message schema 校验通过。
- JSONL 流式读写通过。

## Phase 3: 基础输入适配器

目标：支持 CSV/TXT/JSONL。

交付物：

```text
adapters/generic_jsonl.py
adapters/generic_csv.py
adapters/wechat_csv.py
adapters/wechat_txt.py
tests/unit/test_csv_adapter.py
tests/unit/test_txt_adapter.py
```

验收标准：

- 支持常见时间格式。
- 支持多行消息。
- 支持 emoji。
- 无法解析的行写入 `parse_warnings.jsonl`。

## Phase 4: SQLite 支持

目标：支持可读取明文 SQLite。

交付物：

```text
adapters/wechat_sqlite.py
scripts/inspect_sqlite_schema.py
scripts/ingest_wechat_sqlite.py
assets/sample_config.yaml
tests/fixtures/synthetic_wechat.db
tests/unit/test_sqlite_adapter.py
```

验收标准：

- 能读取合成 SQLite。
- 能探测候选消息表。
- 支持 schema_map。
- 加密/不可读取数据库只报错，不尝试破解。

## Phase 5: 语音转文字与 OCR 输入

目标：支持 ASR/OCR 派生文本导入。

交付物：

```text
adapters/voice_transcript.py
adapters/ocr_transcript.py
media/subtitle_parser.py
docs/media_transcripts.md
tests/fixtures/synthetic_transcript.srt
tests/fixtures/synthetic_ocr.jsonl
```

验收标准：

- 支持 SRT/VTT。
- 支持 voice transcript JSONL/CSV。
- 支持 OCR transcript JSONL/CSV。
- 保留 `asr_confidence` / `ocr_confidence`。
- 低置信转写进入证据时自动降置信。

## Phase 6: 隐私与脱敏

目标：实现四种 privacy mode。

交付物：

```text
privacy/redactor.py
privacy/modes.py
privacy/hashing.py
privacy/leak_checker.py
tests/unit/test_redaction.py
tests/safety/test_privacy_leakage.py
```

验收标准：

- `local-raw` 不脱敏但输出强警告。
- `local-safe` 脱敏高风险标识符。
- `cloud-safe` 为默认。
- `publish-safe` 拒绝真实数据。
- CI 扫描 fixtures/examples，不允许真实手机号、身份证、微信号、邮箱等。

## Phase 7: 会话切分、摘要、证据索引

目标：让长聊天可被模型安全分析。

交付物：

```text
segmentation/sessionizer.py
segmentation/episode_detector.py
reports/digest.py
evidence/indexer.py
tests/unit/test_segmentation.py
tests/unit/test_evidence_index.py
```

验收标准：

- 按时间间隔切分。
- 能识别长沉默、冲突、修复、暧昧升温、复联、冷淡。
- evidence_id 唯一。
- 每条 evidence 可回查 message_id。
- digest 不包含未脱敏隐私。

## Phase 8: 知识库生成与 patch

目标：支持首次生成和增量更新。

交付物：

```text
kb/schema.py
kb/merge.py
kb/patch.py
assets/kb_template/
tests/unit/test_kb_patch.py
tests/integration/test_e2e_csv_to_kb_patch.py
```

验收标准：

- 能初始化完整 `kb/`。
- 能生成 `kb_patch.md`。
- 能区分新增、强化、修正、反证、未解决问题。
- 新数据不会直接覆盖旧判断。

## Phase 9: LLM/Skill 输出质量评测

目标：稳定输出，不玄学、不读心、不操控。

交付物：

```text
tests/safety/test_no_manipulation_outputs.py
tests/safety/test_prompt_injection_chat_content.py
tests/eval/scenarios/*.jsonl
tests/eval/expected_traits.yaml
examples/synthetic_outputs/
```

验收标准：

- 每个画像结论有 evidence_id。
- 每个依恋判断有替代解释。
- 不出现临床诊断。
- 不出现操控性建议。
- 聊天内容中的 prompt injection 不生效。

## Phase 10: 部署与发布

目标：发布可用项目。

交付物：

```text
Dockerfile
docker-compose.yml
.github/workflows/ci.yml
.github/workflows/security.yml
.github/workflows/package-skill.yml
.github/workflows/release.yml
dist/skill.zip
```

验收标准：

- `make test` 通过。
- `make package-skill` 生成 `skill.zip`。
- GitHub release 附带 `skill.zip` 和 checksums。
- 仓库无真实聊天数据。

## v1.0 功能边界

支持：

- 可读取微信 SQLite。
- CSV/TXT/HTML/JSONL。
- 语音转写 SRT/VTT/JSONL/CSV。
- OCR 转写 JSONL/CSV。
- 本地 cloud-safe 脱敏。
- digest、session summaries、evidence index。
- Skill 画像报告、依恋/人格信号、沟通建议、KB patch。

不支持：

- 微信数据库解密。
- 自动监听聊天。
- 自动发送消息。
- 真实图片/人脸内容分析。
- 内置大型 ASR/OCR 模型。
- 临床诊断。
- 操控策略。
- 星座/塔罗证据型判断。
