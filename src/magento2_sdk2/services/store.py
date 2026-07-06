# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from magento2_sdk2.exceptions import MagentoError
from magento2_sdk2.services.client import Magento2Client
from magento2_sdk2.services.request import Request
from magento2_sdk2.validators.response import validate_magento2_response


class StoreService:
    """Service for managing Magento 2 Store Views."""

    client: Magento2Client

    def __init__(self, client: Magento2Client):
        self.client = client

    def get_store_views(self) -> list[dict]:
        """
        Retrieves all store views from Magento.

        Returns:
            List of store view dictionaries with structure:
            [
                {
                    "id": int,
                    "code": str,
                    "name": str,
                    "website_id": int,
                    "store_group_id": int,
                    "is_active": int
                },
                ...
            ]
        """
        try:
            response = self._get_store_views()
            return response if isinstance(response, list) else []
        except Exception as e:
            print(f"Error while fetching store views: {e}")
            return []

    def _get_store_views(self) -> list:
        """
        Executes API request to Magento for store views.

        Returns:
            List of store view dictionaries
        """
        request = Request(
            method="GET",
            resource="V1/store/storeViews",
            auth=self.client,
        )
        response = request.make_request()
        validation, response_body = validate_magento2_response(response, request)

        if validation:
            return response_body
        else:
            raise MagentoError(f"Magento API returned error. Message: {response_body.get('message')}")

    def get_store_view(self, store_code: str) -> tuple[bool, dict]:
        """
        Retrieves details of a specific store view from Magento.

        Args:
            store_code: Store view code

        Returns:
            Tuple (success, response) where success is bool and response is dict
        """
        try:
            request = Request(
                method="GET",
                resource=f"V1/store/storeViews/{store_code}",
                auth=self.client,
            )
            response = request.make_request()
            return validate_magento2_response(response, request)
        except Exception as e:
            print(f"Error while fetching store view: {e}")
            return False, {"error": str(e)}
