# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from magento2_sdk2.exceptions import MagentoError
from magento2_sdk2.services.client import Magento2Client
from magento2_sdk2.services.request import Request
from magento2_sdk2.validators.response import validate_magento2_response


class AttributeSetService:
    """Service for managing Magento 2 Attribute Sets."""

    client: Magento2Client

    def __init__(self, client: Magento2Client):
        self.client = client

    def get_attribute_sets(
        self, store_view: str | None = None, page_size: int = 100, current_page: int = 1
    ) -> list[dict]:
        """
        Retrieves all attribute sets from Magento.

        Args:
            store_view: Optional store view code in Magento
            page_size: Number of items per page (default: 100)
            current_page: Current page number (default: 1)

        Returns:
            List of attribute set dictionaries
        """
        try:
            response = self._get_attribute_sets(store_view, page_size, current_page)
            return response.get("items", [])
        except Exception as e:
            print(f"Error while fetching attribute sets: {e}")
            return []

    def get_all_attribute_sets(self, store_view: str | None = None, page_size: int = 100) -> list[dict]:
        """
        Retrieves all attribute sets from Magento using pagination.

        Args:
            store_view: Optional store view code in Magento
            page_size: Number of items per page (default: 100)

        Returns:
            List of all attribute set dictionaries
        """
        all_items = []
        current_page = 1

        while True:
            response = self._get_attribute_sets(store_view, page_size, current_page)
            items = response.get("items", [])

            if not items:
                break

            all_items.extend(items)

            total_count = response.get("total_count", 0)
            if len(all_items) >= total_count:
                break

            current_page += 1

        return all_items

    def _get_attribute_sets(self, store_view: str | None = None, page_size: int = 100, current_page: int = 1) -> dict:
        """
        Executes single API request to Magento for attribute sets with pagination support.

        Args:
            store_view: Optional store view code in Magento
            page_size: Number of items per page
            current_page: Current page number

        Returns:
            Dict with API response containing items, search_criteria, and total_count
        """
        resource = (
            f"{store_view}/V1/products/attribute-sets/sets/list"
            if store_view
            else "V1/products/attribute-sets/sets/list"
        )

        request = Request(
            method="GET",
            resource=resource,
            auth=self.client,
            params={
                "searchCriteria[pageSize]": page_size,
                "searchCriteria[currentPage]": current_page,
            },
        )

        response = request.make_request()
        validation, response_body = validate_magento2_response(response, request)

        if validation:
            return response_body
        else:
            raise MagentoError(f"Magento API returned error. Message: {response_body.get('message')}")

    def get_attribute_set(self, attribute_set_id: int, store_view: str | None = None) -> tuple[bool, dict]:
        """
        Retrieves details of a specific attribute set from Magento.

        Args:
            attribute_set_id: ID of the attribute set in Magento
            store_view: Optional store view code in Magento

        Returns:
            Tuple (success, response) where success is bool and response is dict
        """
        try:
            resource = (
                f"{store_view}/V1/products/attribute-sets/{attribute_set_id}"
                if store_view
                else f"V1/products/attribute-sets/{attribute_set_id}"
            )

            request = Request(method="GET", resource=resource, auth=self.client)
            response = request.make_request()
            return validate_magento2_response(response, request)
        except Exception as e:
            print(f"Error while fetching attribute set: {e}")
            return False, {"error": str(e)}
