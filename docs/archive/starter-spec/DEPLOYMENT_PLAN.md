# Deployment Plan

## 1. 默认部署：本地预处理 + ChatGPT Skill 分析

这是项目默认路径。

```text
原始数据留在本地
↓
本地 CLI 归一化、脱敏、会话切分、摘要、证据索引
↓
用户上传 cloud-safe 产物给 ChatGPT Skill
↓
Skill 生成报告、建议和 KB patch
```

推荐上传：

```text
work/relationship_digest.redacted.md
work/session_summaries.redacted.jsonl
work/evidence_index.redacted.jsonl
kb/metadata.yaml
kb/*.md, if updating existing KB
```

不推荐上传：

```text
原始数据库
原始导出全文
原始语音
原始截图
未脱敏完整聊天记录
```

## 2. 本地 CLI 安装

开发安装：

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
wri --help
```

## 3. 本地运行流程

```bash
wri init ./my_relationship_project
cd ./my_relationship_project

wri inspect input/chat.db --type sqlite
wri ingest sqlite --db input/chat.db --schema-map config/schema_map.yaml --out work/raw_messages.jsonl
wri normalize --in work/raw_messages.jsonl --out work/normalized_messages.jsonl
wri redact --in work/normalized_messages.jsonl --out work/normalized.cloud-safe.jsonl --privacy-mode cloud-safe
wri segment --in work/normalized.cloud-safe.jsonl --out work/session_summaries.redacted.jsonl
wri digest --messages work/normalized.cloud-safe.jsonl --sessions work/session_summaries.redacted.jsonl --out work/relationship_digest.redacted.md
wri evidence --messages work/normalized.cloud-safe.jsonl --sessions work/session_summaries.redacted.jsonl --out work/evidence_index.redacted.jsonl
```

## 4. ChatGPT Skill 使用流程

1. 上传 `skill.zip` 到 ChatGPT Skills。
2. 新建对话，上传：
   - `relationship_digest.redacted.md`
   - `session_summaries.redacted.jsonl`
   - `evidence_index.redacted.jsonl`
   - 旧 `kb/` 文件，如果需要更新。
3. 请求：

```text
请基于这些本地预处理后的聊天摘要和证据索引，生成对方亲密关系沟通画像、非临床人格沟通信号、依恋焦虑/回避相关信号、互动循环分析、后续沟通建议，并输出 kb_patch。
```

## 5. 完全本地模式

适合对隐私要求极高的用户。

```bash
wri run-local \
  --messages work/normalized_messages.jsonl \
  --privacy-mode local-raw \
  --out reports/
```

注意：

- 本地模式可以关闭脱敏。
- 不要把 `local-raw` 输出上传云端或提交 GitHub。
- 本项目可提供 prompt 模板，但不强绑定某个本地模型。

## 6. Docker 部署

`Dockerfile`：

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY cli ./cli
COPY skill ./skill

RUN pip install --no-cache-dir -e .

ENTRYPOINT ["wri"]
```

`docker-compose.yml`：

```yaml
services:
  wri:
    build: .
    volumes:
      - ./input:/app/input
      - ./work:/app/work
      - ./kb:/app/kb
      - ./reports:/app/reports
    environment:
      - WRI_PRIVACY_MODE=cloud-safe
```

使用：

```bash
docker compose run --rm wri inspect input/chat.db
docker compose run --rm wri ingest sqlite --db input/chat.db --out work/raw_messages.jsonl
docker compose run --rm wri normalize --in work/raw_messages.jsonl --out work/normalized.jsonl
docker compose run --rm wri redact --in work/normalized.jsonl --out work/cloud-safe.jsonl --privacy-mode cloud-safe
docker compose run --rm wri digest --messages work/cloud-safe.jsonl --out work/digest.md
```

## 7. GitHub Actions

### 7.1 CI

`.github/workflows/ci.yml`：

```yaml
name: CI

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"
      - name: Lint
        run: ruff check .
      - name: Type check
        run: mypy cli
      - name: Tests
        run: pytest -q
      - name: Privacy fixture scan
        run: python tools/check_no_real_private_data.py tests examples docs
```

### 7.2 Security

`.github/workflows/security.yml`：

```yaml
name: Security

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install security tools
        run: |
          python -m pip install --upgrade pip
          pip install bandit pip-audit
      - name: Bandit
        run: bandit -r cli skill -x tests
      - name: Pip audit
        run: pip-audit
      - name: Forbidden network scan
        run: python tools/check_no_forbidden_network_calls.py cli skill
```

### 7.3 Package Skill

```yaml
name: Package Skill

on:
  workflow_dispatch:
  push:
    tags:
      - "v*"

permissions:
  contents: read

jobs:
  package:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Validate Skill structure
        run: python tools/validate_skill_structure.py skill
      - name: Package skill
        run: |
          mkdir -p dist
          cd skill
          zip -r ../dist/skill.zip .
      - name: Check size
        run: python tools/check_skill_size.py dist/skill.zip
      - uses: actions/upload-artifact@v4
        with:
          name: skill.zip
          path: dist/skill.zip
```

## 8. Release

Release 必须包含：

```text
skill.zip
source code tarball
checksums.txt
release notes
```

版本建议：

```text
0.9.0 skill skeleton
0.9.0 jsonl/csv/txt pipeline
0.9.0 sqlite support
0.9.0 asr/ocr transcript support
0.9.0 privacy modes
0.9.0 evidence/kb patch
0.9.0 first stable release
```
