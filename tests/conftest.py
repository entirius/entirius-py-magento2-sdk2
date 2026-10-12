# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json

import pytest
from requests import Response

from magento2_sdk2.services.client import Magento2Client

BASE_URL = "https://novatrade.example.com/rest/"


class FakeMagento:
    """Stands in for `requests.request`: serves queued bodies and records the outgoing calls."""

    def __init__(self, payloads: tuple, status_codes: list[int]) -> None:
        self._responses = [self._build(payload, code) for payload, code in zip(payloads, status_codes, strict=True)]
        self.calls: list[dict] = []

    @staticmethod
    def _build(payload, status_code: int) -> Response:
        response = Response()
        response.status_code = status_code
        response.encoding = "utf-8"
        response.headers["Content-Type"] = "application/json"
        response._content = json.dumps(payload).encode()
        return response

    def __call__(self, **kwargs) -> Response:
        self.calls.append(kwargs)
        return self._responses.pop(0)

    @property
    def urls(self) -> list[str]:
        return [call["url"] for call in self.calls]


@pytest.fixture
def magento_client() -> Magento2Client:
    return Magento2Client(base_url=BASE_URL, access_token="kestrel-supply-token")


@pytest.fixture
def fake_magento(monkeypatch):
    """Return an installer taking one response body per expected HTTP call.

    `status_code` is either one code for every body, or one code per body.
    """

    def _install(*payloads, status_code: int | list[int] = 200) -> FakeMagento:
        codes = status_code if isinstance(status_code, list) else [status_code] * len(payloads)
        transport = FakeMagento(payloads, codes)
        monkeypatch.setattr("magento2_sdk2.services.request.requests.request", transport)
        return transport

    return _install
