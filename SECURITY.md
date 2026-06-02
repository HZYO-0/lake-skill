# Security Policy

This project processes sensitive relationship chat data.

## Reporting Vulnerabilities

Please report security vulnerabilities privately to the maintainers.

## Security Guidelines

- Do not upload real chat logs to GitHub issues.
- Do not include personal chat databases in pull requests.
- Do not request help decrypting or bypassing WeChat databases.
- Do not share raw outputs generated in local-raw mode.

## Project Security Features

- Two usage modes: direct paste (quick) and local preprocessing (privacy-first). User chooses.
- Privacy modes: local-raw, local-safe, cloud-safe, publish-safe.
- No telemetry or network upload by default.
- Evidence-based analysis with confidence levels and counterevidence.

## Threat Model

See [PRIVACY_SECURITY.md](PRIVACY_SECURITY.md) for detailed threat model and mitigation strategies.
