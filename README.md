# magento2-sdk2

Magento 2 REST API SDK — products, customers, attributes, search and stores over the Magento 2 REST API.

## Installation

```shell
pip install entirius-py-magento2-sdk2
```

## Usage

```python
from magento2_sdk2.services.client import Magento2Client
from magento2_sdk2.services.worker import search
from magento2_sdk2.dto.search import SearchParameters

client = Magento2Client(base_url="https://your-magento/rest/", access_token="...")
results = search(client, SearchParameters(search_text="shoes"))
```

## Development

```shell
make install     # sync dependencies (uv)
make check       # lint + format check (ruff)
make test        # test suite (pytest) — integration tests skipped without MAGENTO2_URL / MAGENTO2_TOKEN
```

Development and agent instructions: [AGENTS.md](AGENTS.md).

## License

Mozilla Public License 2.0 — see [LICENSE](LICENSE).
