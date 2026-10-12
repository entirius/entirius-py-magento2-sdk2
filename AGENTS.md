# AGENTS.md

Magento 2 REST API SDK — distribution `entirius-py-magento2-sdk2`, import `magento2_sdk2`.

## Commands

| Command | Meaning |
|---|---|
| `make install` | sync dependencies (uv, incl. extras) |
| `make check` | lint + format-check (ruff) |
| `make fix` | auto-fix lint + format |
| `make test` | test suite (pytest) |

## Conventions

- English only: code, docs, commits, branches, PRs.
- MPL-2.0: every non-trivial source file carries the license header (pre-commit inserts it).
- Toolchain: uv + ruff + hatchling + pytest; all config in `pyproject.toml`; `uv.lock` committed.
- Git flow: `master` (production) + `develop` (integration); changes land via PR; semver tag on `master`.
- Never rename the import package `magento2_sdk2` — it is a public API contract.
- Default: do not commit — git is the user's call.
- No AI attribution in commits or PR descriptions.

## Architecture

- `services/client.py` — `Magento2Client`: base URL + auth (Bearer / Basic), SSL toggle.
- `services/request.py` — thin HTTP wrapper over `requests`.
- `services/` — `worker` (search, suggest, customer batch, product variants), `product`, `attribute`,
  `attribute_set`, `store`.
- `dto/` + `domain/` — product, price, media, customer, review, store and search payload dataclasses
  (`marshmallow-dataclass`).
- `validators/` — response shape validation.
- Integration tests hit the live Magento API — skipped unless `MAGENTO2_URL` / `MAGENTO2_TOKEN` are set.
