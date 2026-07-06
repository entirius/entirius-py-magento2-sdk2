# Changelog

All notable changes to this project are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-07-06

Initial public release.

### Added

- `Magento2Client` — Magento 2 REST API client (Bearer / Basic auth, SSL toggle).
- Services: products, attributes, attribute sets, customers, stores and search/suggest workers.
- DTOs for product, price, media, customer, review, store and search payloads; response validators.
- Toolchain: uv (env + lock), ruff (lint + format), hatchling (build), pytest;
  MPL-2.0 with per-file headers; pre-commit + CI (lint, test, secret-scan).
