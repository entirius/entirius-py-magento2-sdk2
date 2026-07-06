# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


class Magento2Client:
    base_url: str
    access_token: str
    access_type: str = "Bearer"
    requires_auth: bool = True
    verify_ssl: bool = True

    def __init__(
        self,
        base_url: str,
        access_token: str,
        requires_auth: bool = True,
        access_type: str = "Bearer",
        verify_ssl: bool = True,
    ) -> None:
        self.base_url = base_url
        self.access_token = access_token
        self.access_type = access_type
        self.requires_auth = requires_auth
        self.verify_ssl = verify_ssl

    def make_url_without_rest(self):
        url = self.base_url.split("rest")
        if url:
            self.base_url = url[0]
