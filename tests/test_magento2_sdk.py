# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import traceback
from base64 import b64encode

import pytest
from faker import Faker

from magento2_sdk2.dto.customer import CustomerData, MainCustomerData
from magento2_sdk2.dto.search import BaseParams, SearchParameters, SearchResult, SuggestParameters
from magento2_sdk2.services.client import Magento2Client
from magento2_sdk2.services.worker import batch_customer_post, get_customers, search, suggest

MAGENTO_BASIC_AUTH_LOGIN = os.environ.get("MAGENTO2_BASIC_AUTH_LOGIN", "")
MAGENTO_BASIC_AUTH_PASSWORD = os.environ.get("MAGENTO2_BASIC_AUTH_PASSWORD", "")
MAGENTO2_URL_FOR_CHECKOUT_EXPORT = os.environ.get("MAGENTO2_URL", "")
MAGENTO2_TOKEN_FOR_CHECKOUT_EXPORT = os.environ.get("MAGENTO2_TOKEN", "")

pytestmark = pytest.mark.skipif(
    not (MAGENTO2_URL_FOR_CHECKOUT_EXPORT and MAGENTO2_TOKEN_FOR_CHECKOUT_EXPORT),
    reason="Magento credentials not set (MAGENTO2_URL, MAGENTO2_TOKEN env vars)",
)


def test_get_id_product():
    magento_client: Magento2Client = Magento2Client(
        base_url=MAGENTO2_URL_FOR_CHECKOUT_EXPORT, access_token=MAGENTO2_TOKEN_FOR_CHECKOUT_EXPORT
    )
    search_params_obj = SearchParameters(search_text="a")
    try:
        response = search(magento_client, search_params_obj)
    except Exception as e:
        print(str(e))


def test_get_suggest_term_and_products_id():
    credentials_b64 = b64encode(f"{MAGENTO_BASIC_AUTH_LOGIN}:{MAGENTO_BASIC_AUTH_PASSWORD}".encode()).decode()
    magento_client: Magento2Client = Magento2Client(
        base_url=MAGENTO2_URL_FOR_CHECKOUT_EXPORT, access_token=credentials_b64, access_type="Basic"
    )
    search_params_obj = SuggestParameters(q="śru")
    try:
        response = suggest(magento_client, search_params_obj)
        search_results = []
        for each in response:
            search_results.append(SearchResult.Schema().load(each))

    except Exception as e:
        print(str(e))


def test_get_customers():
    magento_client: Magento2Client = Magento2Client(
        base_url=MAGENTO2_URL_FOR_CHECKOUT_EXPORT, access_token=MAGENTO2_TOKEN_FOR_CHECKOUT_EXPORT
    )
    search_obj = BaseParams(page_size=999, current_page=1)
    try:
        response = get_customers(magento_client, search_obj)
        print(response)
    except Exception as e:
        print(str(e))


def test_batch_post_customer():
    magento_client: Magento2Client = Magento2Client(
        base_url=MAGENTO2_URL_FOR_CHECKOUT_EXPORT, access_token=MAGENTO2_TOKEN_FOR_CHECKOUT_EXPORT
    )
    faker = Faker()
    search_obj = [
        MainCustomerData(
            customer=CustomerData(
                email=faker.email(), firstname=faker.first_name(), lastname=faker.last_name(), addresses=[]
            )
        )
        for i in range(1)
    ]

    try:
        response = batch_customer_post(magento_client, search_obj)
        print(response)
    except Exception as e:
        traceback.print_exc()
