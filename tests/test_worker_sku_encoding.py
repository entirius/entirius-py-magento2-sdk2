# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from magento2_sdk2.services.worker import get_product, get_product_variants


def test_get_product_url_encodes_a_sku_containing_a_slash(magento_client, fake_magento):
    transport = fake_magento({"sku": "ENT-100/A"})

    get_product(magento_client, "default", "ENT-100/A")

    assert transport.urls == ["https://novatrade.example.com/rest/default/V1/products/ENT-100%2FA"]


def test_get_product_variants_url_encodes_a_sku_containing_a_slash(magento_client, fake_magento):
    transport = fake_magento([])

    get_product_variants(magento_client, "default", "ENT-100/A")

    assert transport.urls == ["https://novatrade.example.com/rest/default/V1/productVariants/ENT-100%2FA"]
