# entirius-py-magento2-sdk2

A Python client for the catalog side of the Magento 2 REST API, part of
Entirius, the open-source modular ecommerce platform. It covers products, prices, pictures, attributes, customers,
stores and search, with typed payloads.

[![PyPI](https://img.shields.io/pypi/v/entirius-py-magento2-sdk2.svg)](https://pypi.org/project/entirius-py-magento2-sdk2/)
[![Python](https://img.shields.io/pypi/pyversions/entirius-py-magento2-sdk2.svg)](https://pypi.org/project/entirius-py-magento2-sdk2/)
[![License: MPL-2.0](https://img.shields.io/badge/license-MPL--2.0-blue.svg)](https://github.com/entirius/entirius-py-magento2-sdk2/blob/develop/LICENSE)

## What it does

- Saves products, product attributes, prices and special prices, one at a time or in batches.
- Uploads product pictures and reads store views, websites, attribute sets and categories.
- Reads, updates and deletes product attributes and adds attribute options.
- Searches and suggests products, and posts customers in batches.
- Authorizes with a Bearer token or Basic credentials; SSL verification can be switched off for test stores.

## Installation

```shell
uv add entirius-py-magento2-sdk2
pip install entirius-py-magento2-sdk2
```

The import name is `magento2_sdk2`.

## Quick start

```python
from magento2_sdk2.services.client import Magento2Client
from magento2_sdk2.services.worker import search
from magento2_sdk2.dto.search import SearchParameters

client = Magento2Client(base_url="https://magento.example.com/rest/", access_token="...")
results = search(client, SearchParameters(search_text="shoes"))
```

## Requirements

- Python 3.11 or newer.
- `requests`, `marshmallow`, `marshmallow-dataclass` (installed as dependencies).
- A Magento 2 store with a REST API integration token.

## Documentation

- Entirius documentation: https://docs.entirius.com/
- Changelog: https://github.com/entirius/entirius-py-magento2-sdk2/blob/develop/CHANGELOG.md

## Part of Entirius

This SDK is the catalog and customer client of the bridges that connect the Entirius backend service (Volkanos) to an
existing Magento 2 store.

- Backend service: https://github.com/entirius/entirius-service-volkanos
- Docker harness: https://github.com/entirius/entirius-zeno
- Bridges that use it: https://github.com/entirius/entirius-django-pim-export-to-magento-api,
  https://github.com/entirius/entirius-django-accounts-export-to-magento-api
- Sibling SDK (the order side): https://github.com/entirius/entirius-py-magento2-sdk

## Development

```shell
make install     # sync dependencies (uv)
make check       # lint + format check (ruff)
make test        # test suite (pytest); the integration tests are skipped without MAGENTO2_URL / MAGENTO2_TOKEN
```

Development and agent instructions: https://github.com/entirius/entirius-py-magento2-sdk2/blob/develop/AGENTS.md

## License

Mozilla Public License 2.0 (MPL-2.0) — see https://github.com/entirius/entirius-py-magento2-sdk2/blob/develop/LICENSE.
