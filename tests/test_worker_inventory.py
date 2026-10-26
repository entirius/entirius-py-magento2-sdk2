# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from magento2_sdk2.exceptions import MagentoError
from magento2_sdk2.services.worker import get_product_salable_quantity, get_source_items_batch


def test_get_product_salable_quantity_returns_the_quantity_reported_by_magento(magento_client, fake_magento):
    fake_magento(7.5)

    assert get_product_salable_quantity(magento_client, "ENT-100", 2) == 7.5


def test_get_product_salable_quantity_asks_for_one_stock_and_encodes_the_sku(magento_client, fake_magento):
    transport = fake_magento(0)

    get_product_salable_quantity(magento_client, "ENT-100/A", 2)

    assert transport.urls == [
        "https://novatrade.example.com/rest/V1/inventory/get-product-salable-quantity/ENT-100%2FA/2"
    ]


def test_get_source_items_batch_maps_each_sku_to_a_float_quantity(magento_client, fake_magento):
    fake_magento(
        {
            "items": [
                {"sku": "ENT-100", "quantity": "3.5"},
                {"sku": "ENT-200", "quantity": 12},
                {"sku": "ENT-300", "quantity": None},
            ]
        }
    )

    quantities = get_source_items_batch(magento_client, "kestrel_supply")

    assert quantities == {"ENT-100": 3.5, "ENT-200": 12.0, "ENT-300": 0.0}


def test_get_source_items_batch_filters_the_search_by_source_code(magento_client, fake_magento):
    transport = fake_magento({"items": []})

    get_source_items_batch(magento_client, "kestrel_supply")

    params = transport.calls[0]["params"]
    assert params["searchCriteria[filterGroups][0][filters][0][field]"] == "source_code"
    assert params["searchCriteria[filterGroups][0][filters][0][value]"] == "kestrel_supply"


def test_get_source_items_batch_walks_pages_until_a_short_one(magento_client, fake_magento):
    transport = fake_magento(
        {"items": [{"sku": "ENT-100", "quantity": 1}, {"sku": "ENT-200", "quantity": 2}]},
        {"items": [{"sku": "ENT-300", "quantity": 3}]},
    )

    quantities = get_source_items_batch(magento_client, "kestrel_supply", page_size=2)

    assert quantities == {"ENT-100": 1.0, "ENT-200": 2.0, "ENT-300": 3.0}
    assert [
        (call["params"]["searchCriteria[currentPage]"], call["params"]["searchCriteria[pageSize]"])
        for call in transport.calls
    ] == [(1, 2), (2, 2)]


def test_get_source_items_batch_stops_at_total_count_when_the_last_page_is_full(magento_client, fake_magento):
    full_page = {"items": [{"sku": "ENT-100", "quantity": 1}, {"sku": "ENT-200", "quantity": 2}], "total_count": 2}
    transport = fake_magento(full_page, full_page)

    quantities = get_source_items_batch(magento_client, "kestrel_supply", page_size=2)

    assert quantities == {"ENT-100": 1.0, "ENT-200": 2.0}
    assert len(transport.calls) == 1


def test_get_source_items_batch_skips_rows_without_a_sku(magento_client, fake_magento):
    fake_magento({"items": [{"sku": "ENT-100", "quantity": 1}, {"quantity": 9}]})

    assert get_source_items_batch(magento_client, "kestrel_supply") == {"ENT-100": 1.0}


def test_get_source_items_batch_raises_instead_of_returning_a_partial_sweep(magento_client, fake_magento):
    fake_magento(
        {"items": [{"sku": "ENT-100", "quantity": 1}]},
        {"message": "Source kestrel_supply is not available"},
        status_code=[200, 409],
    )

    with pytest.raises(MagentoError, match="Source kestrel_supply is not available"):
        get_source_items_batch(magento_client, "kestrel_supply", page_size=1)
