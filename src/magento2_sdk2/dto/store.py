# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from dataclasses import dataclass

from magento2_sdk2.dto import DTO


@dataclass
class Store(DTO):
    id: int
    code: str
    name: str
    website_id: int
    store_group_id: int
    is_active: int
