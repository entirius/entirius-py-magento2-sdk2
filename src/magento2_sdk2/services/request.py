# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import requests
from requests import Response

from magento2_sdk2.services.client import Magento2Client


class Request:
    method: str
    resource: str
    auth: Magento2Client
    headers: dict | None
    params: dict | None
    body: dict | None
    json: dict | None

    def create_headers(self):
        if type(self.headers) != dict:
            self.headers = {}
        self.headers["Content-Type"] = "application/json; charset=utf-8"
        self.headers["Accept"] = "application/json"

    def __init__(
        self,
        method: str,
        auth: Magento2Client,
        resource: str,
        params=None,
        headers: dict = None,
        body: dict = None,
        json: dict | list = None,
    ):
        self.method = method
        self.auth = auth
        self.headers = headers
        self.params = params
        self.resource = resource
        self.body = body
        self.json = json
        self.url = self._build_url()

    def authorize(self):
        if type(self.headers) != dict:
            self.headers = {}
        if self.auth.requires_auth:
            self.headers["Authorization"] = f"{self.auth.access_type} {self.auth.access_token}"

    def make_parameters(self):
        self.authorize()
        self.create_headers()
        params = {"params": self.params, "headers": self.headers}
        function_params = {k: v for (k, v) in params.items() if v}
        return function_params

    def _build_url(self) -> str:
        return self.auth.base_url + self.resource

    def make_request(self) -> Response:
        function_params = self.make_parameters()
        params = {
            "method": self.method,
            "url": self._build_url(),
            "data": self.body,
            "params": function_params.get("params", None),
            "headers": function_params.get("headers", None),
            "json": self.json,
            "verify": self.auth.verify_ssl,
        }
        function_params = {k: v for (k, v) in params.items() if v is not None}
        res = requests.request(**function_params)
        return res
