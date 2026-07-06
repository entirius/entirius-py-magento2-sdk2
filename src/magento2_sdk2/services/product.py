# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from magento2_sdk2.dto.media import Media
from magento2_sdk2.dto.price import SpecialPrice
from magento2_sdk2.dto.product import Product as ProductDTO
from magento2_sdk2.dto.product import ProductLite, ProductPrice
from magento2_sdk2.dto.store import Store
from magento2_sdk2.exceptions import MagentoError
from magento2_sdk2.services.attribute import Attribute
from magento2_sdk2.services.client import Magento2Client
from magento2_sdk2.services.request import Request
from magento2_sdk2.validators.response import validate_magento2_response


class Product:
    client: Magento2Client

    def __init__(self, client: Magento2Client):
        self.client = client

    def get_attributes(self, store_view: str | None = None) -> list:
        attribute_service = Attribute(self.client)
        return attribute_service.get_attributes(store_view)

    def save_product(self, product: ProductDTO, store_view: str = "all") -> tuple[bool, dict]:
        request = Request(
            method="POST",
            resource=f"{store_view}/V1/products",
            auth=self.client,
            json={"product": product.asdict_for_create()},
        )
        response = request.make_request()
        return validate_magento2_response(response, request)

    def save_product_attributes(self, product: ProductLite, store_view: str = "all") -> tuple[bool, dict]:
        request = Request(
            method="POST", resource=f"{store_view}/V1/products", auth=self.client, json={"product": product.asdict()}
        )
        response = request.make_request()
        return validate_magento2_response(response, request)

    def save_product_price(self, product: ProductPrice, store_view: str = "all") -> tuple[bool, dict]:
        request = Request(
            method="POST", resource=f"{store_view}/V1/products", auth=self.client, json={"product": product.asdict()}
        )
        response = request.make_request()
        return validate_magento2_response(response, request)

    def save_products(self, products: list[ProductDTO], store_view: str = "all") -> tuple[bool, dict]:
        request = Request(
            method="POST",
            resource=f"{store_view}/async/bulk/V1/products",
            auth=self.client,
            json=[{"product": product.asdict_for_create()} for product in products],
        )
        response = request.make_request()
        return validate_magento2_response(response, request)

    def save_products_attributes(self, products: list[ProductLite], store_view: str = "all") -> tuple[bool, dict]:
        request = Request(
            method="POST",
            resource=f"{store_view}/async/bulk/V1/products",
            auth=self.client,
            json=[{"product": product.asdict()} for product in products],
        )
        response = request.make_request()
        return validate_magento2_response(response, request)

    def save_products_prices(self, products: list[ProductPrice], store_view: str = "all") -> tuple[bool, dict]:
        request = Request(
            method="POST",
            resource=f"{store_view}/async/bulk/V1/products",
            auth=self.client,
            json=[{"product": product.asdict()} for product in products],
        )
        response = request.make_request()
        return validate_magento2_response(response, request)

    def get_store_websites(self):
        request = Request(method="GET", resource="V1/store/storeViews", auth=self.client)
        response = request.make_request()
        validation, response_body = validate_magento2_response(response, request)

        if validation:
            return response_body
        else:
            raise MagentoError(f"The magento API responded with an error. Message: {response_body.get('message')}")

    def get_store_websites_group_by_id(self) -> dict[int, Store]:
        result = self.get_store_websites()
        stores = {}
        for r in result:
            s = Store(**r)
            stores[s.id] = s
        return stores

    def get_store_websites_group_by_code(self) -> dict[str, Store]:
        result = self.get_store_websites()
        stores = {}
        for r in result:
            s = Store(**r)
            stores[s.code] = s
        return stores

    def save_product_picture(self, sku: str, media: Media, store_view: str | None = None) -> tuple[bool, dict]:
        request = Request(
            method="POST",
            resource=f"{store_view}/V1/products/{sku}/media" if store_view else f"/V1/products/{sku}/media",
            auth=self.client,
            json={"entry": media.asdict()},
        )

        response = request.make_request()
        return validate_magento2_response(response, request)

    def save_special_prices(self, special_prices: list[SpecialPrice], store_view: str = "all") -> tuple[bool, dict]:
        request = Request(
            method="POST",
            resource=f"{store_view}/V1/products/special-price",
            auth=self.client,
            json={"prices": [special_price.asdict_by(store_view) for special_price in special_prices]},
        )
        response = request.make_request()
        return validate_magento2_response(response, request)

    def save_special_price(self, special_price: SpecialPrice, store_view: str = "all") -> tuple[bool, dict]:
        request = Request(
            method="POST",
            resource=f"{store_view}/V1/products/special-price",
            auth=self.client,
            json={"prices": [special_price.asdict_by(store_view)]},
        )
        response = request.make_request()
        return validate_magento2_response(response, request)
