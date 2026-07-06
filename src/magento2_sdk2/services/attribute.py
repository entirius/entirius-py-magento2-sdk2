# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from magento2_sdk2.exceptions import MagentoError
from magento2_sdk2.services.client import Magento2Client
from magento2_sdk2.services.request import Request
from magento2_sdk2.validators.response import validate_magento2_response


class Attribute:
    client: Magento2Client

    def __init__(self, client: Magento2Client):
        self.client = client

    def get_attributes(self, store_view: str | None = None) -> list:
        """
        Pobiera wszystkie atrybuty produktów z Magento.
        Zwraca listę atrybutów bez walidacji (sama lista, nie tuple).
        """
        try:
            response = self._get_attributes(store_view)
            return response.get("items", [])
        except Exception as e:
            print(f"Błąd podczas pobierania atrybutów: {e}")
            return []

    def _get_attributes(self, store_view: str | None = None) -> dict:
        """
        Wykonuje pojedyncze zapytanie do API Magento o atrybuty produktów z obsługą paginacji.
        """
        request = Request(
            method="GET",
            resource=f"{store_view}/V1/products/attributes" if store_view else "V1/products/attributes",
            auth=self.client,
            params={
                "searchCriteria[currentPage]": 1
            },  # magento nie umie w paginacje na tym endpoincie wiec wyciagamy wszystko
        )
        response = request.make_request()
        validation, response_body = validate_magento2_response(response, request)

        if validation:
            return response_body
        else:
            raise MagentoError(f"API Magento zwróciło błąd. Wiadomość: {response_body.get('message')}")

    def get_attribute(self, attribute_id, store_view: str | None = None):
        """
        Pobiera szczegóły atrybutu z Magento.

        Args:
            attribute_id: ID atrybutu w Magento
            store_view: storeview code w Magento

        Returns:
            Tuple (success, response) gdzie success to bool, a response to dict
        """
        try:
            request = Request(
                method="GET",
                resource=(
                    f"{store_view}/V1/products/attributes/{attribute_id}"
                    if store_view
                    else f"V1/products/attributes/{attribute_id}"
                ),
                auth=self.client,
            )
            response = request.make_request()
            return validate_magento2_response(response, request)
        except Exception as e:
            print(f"Błąd podczas pobierania atrybutu: {e}")
            return False, {"error": str(e)}

    def update_attribute(self, attribute_id, attribute_data):
        """
        Aktualizuje istniejący atrybut w Magento.

        Args:
            attribute_id: ID atrybutu w Magento
            attribute_data: Dane atrybutu do aktualizacji

        Returns:
            Tuple (success, response) gdzie success to bool, a response to dict
        """
        try:
            request = Request(
                method="PUT", resource=f"V1/products/attributes/{attribute_id}", auth=self.client, json=attribute_data
            )
            response = request.make_request()
            return validate_magento2_response(response, request)
        except Exception as e:
            print(f"Błąd podczas aktualizacji atrybutu: {e}")
            return False, {"error": str(e)}

    def add_attribute_options(self, attribute_code, options_data):
        """
        Dodaje nowe opcje do istniejącego atrybutu w Magento.

        Args:
            attribute_code: Kod atrybutu w Magento
            options_data: Dane opcji do dodania

        Returns:
            Tuple (success, response) gdzie success to bool, a response to dict
        """
        try:
            request = Request(
                method="POST",
                resource=f"V1/products/attributes/{attribute_code}/options",
                auth=self.client,
                json=options_data,
            )
            response = request.make_request()
            return validate_magento2_response(response, request)
        except Exception as e:
            print(f"Błąd podczas dodawania opcji atrybutu: {e}")
            return False, {"error": str(e)}

    def delete_attribute(self, attribute_code: str) -> tuple[bool, dict]:
        """
        Usuwa atrybut produktu z Magento.

        Args:
            attribute_code: Kod atrybutu do usunięcia

        Returns:
            Tuple z informacją o poprawności (bool) i odpowiedzią z API (dict)
        """
        request = Request(method="DELETE", resource=f"V1/products/attributes/{attribute_code}", auth=self.client)
        response = request.make_request()
        return validate_magento2_response(response, request)
