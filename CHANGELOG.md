# Changelog

All notable changes to this project are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0rc1] - 2026-10-26

### Added

- `get_product_salable_quantity(client, sku, stock_id)`: MSI salable quantity of a SKU in one stock
  (`V1/inventory/get-product-salable-quantity`), reservations included. `V1/stockItems` only reports the legacy
  default-source figure.
- `get_source_items_batch(client, source_code, page_size=200)`: `{sku: quantity}` for every SKU of one MSI source in
  a paginated sweep (`V1/inventory/source-items`). Raw source quantity, not salable quantity.

### Fixed

- `get_product` and `get_product_variants` URL-encode the SKU (`ENT-100/A` → `ENT-100%2FA`); a SKU with a slash
  failed. The Magento host must accept encoded slashes in the path (Apache `AllowEncodedSlashes NoDecode`).

### Changed

- Package metadata: keywords, classifiers and project URLs (docs, changelog, issues) for the PyPI page.

## [2.0.0] - 2026-07-06

Initial public release.

### Added

- `Magento2Client` — Magento 2 REST API client (Bearer / Basic auth, SSL toggle).
- Services: products, attributes, attribute sets, customers, stores and search/suggest workers.
- DTOs for product, price, media, customer, review, store and search payloads; response validators.
- Toolchain: uv (env + lock), ruff (lint + format), hatchling (build), pytest;
  MPL-2.0 with per-file headers; pre-commit + CI (lint, test, secret-scan).
