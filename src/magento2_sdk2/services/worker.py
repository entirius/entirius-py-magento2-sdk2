# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
import logging
from dataclasses import asdict
from urllib.parse import quote

from magento2_sdk2.dto.customer import MainCustomerData
from magento2_sdk2.dto.search import BaseParams, Filter, SearchParameters, SuggestParameters
from magento2_sdk2.exceptions import MagentoError
from magento2_sdk2.services.client import Magento2Client
from magento2_sdk2.services.request import Request
from magento2_sdk2.validators.response import (
    validate_magento2_customer_create_batch,
    validate_magento2_response,
    validate_magento2_reviews,
    validate_magento2_search,
)

logger_process = logging.getLogger("process")


def search(client: Magento2Client, search_obj: SearchParameters, get_full_response=False):
    # each function create diffrent params
    # TODO przenieść searcha do funkcji classy Magento2Client
    search_obj.create_filters()
    if get_full_response:
        search_obj.create_field_parameter("items[id]")
    search_obj.create_type_search_parameters()
    search_obj.create_page_parameters()
    search_obj.create_filter_parameters()

    request = Request(method="GET", resource="V1/search", auth=client, params=search_obj.request_params)
    response = request.make_request()
    validation, response_body = validate_magento2_response(response, request)
    if validation:
        success, missing_keys = validate_magento2_search(response_body)
        if success:
            return response_body
        else:
            logger_process.error(
                "Magento API response failed",
                extra={"details": {"request_params": request.params, "response_body": response_body}},
            )
            raise MagentoError(f"Magento response is not correct. Missing {', '.join(missing_keys)}")
    else:
        raise MagentoError(f"The magento API responded with an error. Message: {response_body.get('message')}")


def get_customers(client: Magento2Client, search_obj: BaseParams):
    search_obj.create_field_parameter("items[email]")
    search_obj.create_page_parameters()
    search_obj.create_filter_parameters()

    request = Request(method="GET", resource="V1/customers/search", auth=client, params=search_obj.request_params)
    response = request.make_request()
    validation, response_body = validate_magento2_response(response, request)
    if validation:
        success, missing_keys = validate_magento2_search(response_body)
        if success:
            return response_body
        else:
            logger_process.error(
                "Magento API response failed",
                extra={"details": {"request_params": request.params, "response_body": response_body}},
            )
            raise MagentoError(f"Magento response is not correct. Missing {', '.join(missing_keys)}")
    else:
        raise MagentoError(f"The magento API responded with an error. Message: {response_body.get('message')}")


def batch_customer_post(client: Magento2Client, customers_data: list[MainCustomerData]):
    data = json.dumps([asdict(customer) for customer in customers_data])
    request = Request(method="POST", resource="async/bulk/V1/customers", auth=client, body=data)
    response = request.make_request()
    validation, response_body = validate_magento2_response(response, request)
    if validation:
        success, missing_keys = validate_magento2_customer_create_batch(response_body)
        if success:
            return response_body, request
        else:
            logger_process.error(
                "Magento API response failed",
                extra={"details": {"request_params": request.params, "response_body": response_body}},
            )
            raise MagentoError(f"Magento response is not correct. Missing {', '.join(missing_keys)}")
    else:
        raise MagentoError(f"The magento API responded with an error. Message: {response_body.get('message')}")


def create_review(self, data):
    request = Request(method="POST", resource="V1/reviews", auth=self, body=json.dumps(asdict(data)))
    response = request.make_request()
    validation, response_body = validate_magento2_response(response, request)
    if validation:
        success, missing_keys = validate_magento2_reviews(response_body)
        if success:
            return response_body
        else:
            logger_process.error(
                "Magento API response failed",
                extra={"details": {"request_params": request.params, "response_body": response_body}},
            )
            raise MagentoError(f"Magento response is not correct. Missing {', '.join(missing_keys)}")
    else:
        raise MagentoError(f"The magento API responded with an error. Message: {response_body.get('message')}")


def suggest(client: Magento2Client, search_obj: SuggestParameters):
    client.make_url_without_rest()
    request = Request(method="GET", resource="search/ajax/suggest/", auth=client, params=asdict(search_obj))
    response = request.make_request()
    validation, response_body = validate_magento2_response(response, request)

    if validation:
        return response_body
    else:
        raise MagentoError(f"The magento API responded with an error. Message: {response_body.get('message')}")


def get_categories(client: Magento2Client, store_view: str):
    request = Request(method="GET", resource=f"{store_view}/V1/categories", auth=client)
    response = request.make_request()
    validation, response_body = validate_magento2_response(response, request)

    if validation:
        return response_body
    else:
        raise MagentoError(f"The magento API responded with an error. Message: {response_body.get('message')}")


def get_category(client: Magento2Client, store_view: str, category_id: int):
    request = Request(method="GET", resource=f"{store_view}/V1/categories/{category_id}", auth=client)
    response = request.make_request()
    validation, response_body = validate_magento2_response(response, request)

    if validation:
        return response_body
    else:
        raise MagentoError(f"The magento API responded with an error. Message: {response_body.get('message')}")


def get_products_in_category(client: Magento2Client, store_view: str, category_id: int):
    request = Request(method="GET", resource=f"{store_view}/V1/categories/{category_id}/products", auth=client)
    response = request.make_request()
    validation, response_body = validate_magento2_response(response, request)

    if validation:
        return response_body
    else:
        raise MagentoError(f"The magento API responded with an error. Message: {response_body.get('message')}")


def post_product_in_category(
    client: Magento2Client, category_id: int, sku: str, position: int = 0, store_view: str = "all"
):
    data = {"productLink": {"sku": sku, "position": position, "category_id": category_id}}
    request = Request(
        method="POST", resource=f"{store_view}/V1/categories/{category_id}/products", auth=client, json=data
    )
    response = request.make_request()
    validation, response_body = validate_magento2_response(response, request)

    if validation:
        return response_body
    else:
        raise MagentoError(f"The magento API responded with an error. Message: {response_body.get('message')}")


def get_products(
    client: Magento2Client,
    store_view: str,
    current_page=1,
    page_size=100,
    product_type: list[str] = None,
    filters: list[Filter] = None,
):
    filters = [] if filters is None else filters
    product_filter = {}
    n = 0  # Enumeration on filterGroups is AND, in filters is OR
    if product_type:
        product_filter[f"searchCriteria[filterGroups][{str(n)}][filters][0][field]"] = "type_id"
        product_filter[f"searchCriteria[filterGroups][{str(n)}][filters][0][condition_type]"] = "in"
        product_filter[f"searchCriteria[filterGroups][{str(n)}][filters][0][value]"] = ",".join(product_type)
        n += 1

    for f in filters:
        product_filter[f"searchCriteria[filterGroups][{str(n)}][filters][0][field]"] = f.field
        product_filter[f"searchCriteria[filterGroups][{str(n)}][filters][0][condition_type]"] = f.condition_type
        product_filter[f"searchCriteria[filterGroups][{str(n)}][filters][0][value]"] = f.value
        n += 1

    request = Request(
        method="GET",
        resource=f"{store_view}/V1/products",
        auth=client,
        params={"searchCriteria[currentPage]": current_page, "searchCriteria[pageSize]": page_size, **product_filter},
    )
    response = request.make_request()
    validation, response_body = validate_magento2_response(response, request)

    if validation:
        return response_body
    else:
        raise MagentoError(f"The magento API responded with an error. Message: {response_body.get('message')}")


def get_stock_item(client: Magento2Client, sku: str):
    """Get stock item data for a product by SKU using dedicated stock API endpoint."""
    # SKU bywa ze slashem - musi być URL-encoded ("/" -> "%2F"),
    # inaczej Magento zwraca "Request does not match any route".
    request = Request(method="GET", resource=f"V1/stockItems/{quote(sku, safe='')}", auth=client)
    response = request.make_request()
    validation, response_body = validate_magento2_response(response, request)

    if validation:
        return response_body
    else:
        raise MagentoError(f"The magento API responded with an error. Message: {response_body.get('message')}")


def get_stock_items_batch(client: Magento2Client, skus: list[str]) -> dict[str, dict]:
    """Get stock items for multiple SKUs by fetching them individually.

    This is a workaround since Magento API doesn't provide a proper bulk endpoint for stock items.
    Returns a dictionary mapping SKU to stock_item data.

    Args:
        client: Magento2Client instance
        skus: List of SKUs to fetch stock items for

    Returns:
        Dict mapping SKU to stock item data: {sku: {item_id, product_id, stock_id, qty, ...}}
    """
    stock_items = {}

    for sku in skus:
        try:
            stock_item = get_stock_item(client, sku)
            if stock_item:
                stock_items[sku] = stock_item
        except Exception as e:
            logger_process.exception(e)
            continue

    return stock_items


def get_product_salable_quantity(client: Magento2Client, sku: str, stock_id: int) -> float:
    """Salable quantity of a SKU in one MSI stock.

    V1/stockItems returns the legacy pre-MSI number: always stock_id 1, taken from the
    default source. On a catalogue with several sources that is the warehouse total, not
    what a given storefront may sell. This endpoint answers per stock and already accounts
    for reservations on unshipped orders.

    Args:
        client: Magento2Client instance
        sku: product SKU (slashes are URL-encoded, Magento rejects raw ones)
        stock_id: MSI stock id (see V1/inventory/stocks)
    """
    request = Request(
        method="GET",
        resource=f"V1/inventory/get-product-salable-quantity/{quote(sku, safe='')}/{stock_id}",
        auth=client,
    )
    response = request.make_request()
    validation, response_body = validate_magento2_response(response, request)

    if validation:
        return response_body
    else:
        raise MagentoError(f"The magento API responded with an error. Message: {response_body.get('message')}")


def get_source_items_batch(client: Magento2Client, source_code: str, page_size: int = 200) -> dict[str, float]:
    """Quantities of every SKU assigned to one MSI source, in a single paginated sweep.

    The salable-quantity endpoint answers per SKU, so a full catalogue would cost one
    request per product. Source items are searchable, so the same data comes in a handful
    of requests. Source quantity is not salable quantity: it is the raw figure for a single
    source, before stock aggregation, reservations and the out-of-stock threshold.

    Args:
        client: Magento2Client instance
        source_code: MSI source code (see V1/inventory/sources)
        page_size: rows per request

    Returns:
        Dict mapping SKU to quantity: {sku: quantity}
    """
    quantities: dict[str, float] = {}
    current_page = 1

    while True:
        request = Request(
            method="GET",
            resource="V1/inventory/source-items",
            auth=client,
            params={
                "searchCriteria[filterGroups][0][filters][0][field]": "source_code",
                "searchCriteria[filterGroups][0][filters][0][condition_type]": "eq",
                "searchCriteria[filterGroups][0][filters][0][value]": source_code,
                "searchCriteria[currentPage]": current_page,
                "searchCriteria[pageSize]": page_size,
            },
        )
        response = request.make_request()
        validation, response_body = validate_magento2_response(response, request)

        if not validation:
            raise MagentoError(f"The magento API responded with an error. Message: {response_body.get('message')}")

        items = response_body.get("items") or []
        for item in items:
            sku = item.get("sku")
            if sku is not None:
                quantities[sku] = float(item.get("quantity") or 0)

        if not items or len(items) < page_size:
            break
        current_page += 1

    return quantities


def get_product(client: Magento2Client, store_view: str, sku: str):
    request = Request(method="GET", resource=f"{store_view}/V1/products/{quote(sku, safe='')}", auth=client)
    response = request.make_request()
    validation, response_body = validate_magento2_response(response, request)

    if validation:
        return response_body
    else:
        raise MagentoError(f"The magento API responded with an error. Message: {response_body.get('message')}")


def get_product_variants(client: Magento2Client, store_view: str, sku: str) -> list:
    """Get product variant groups for a single SKU (custom Magento product-variants module).

    Returns a list of variant groups for the product. Each group has the shape:
        {"label": "Gramatura", "values": [
            {"sku": "0000000750", "attribute_text": "3g", "class": "selected", "swatch_type": 0, "path": "#"},
            ...
        ]}
    The list is empty when the product has no variant groups. Raises on transport/API errors;
    callers that sweep many SKUs should catch per-SKU exceptions and continue (see get_stock_items_batch).
    """
    request = Request(method="GET", resource=f"{store_view}/V1/productVariants/{quote(sku, safe='')}", auth=client)
    response = request.make_request()
    validation, response_body = validate_magento2_response(response, request)

    if validation:
        return response_body
    else:
        raise MagentoError(f"The magento API responded with an error. Message: {response_body.get('message')}")
