# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from dataclasses import dataclass
from decimal import Decimal

from magento2_sdk2.dto import DTO


@dataclass
class SpecialPrice(DTO):
    price: Decimal
    store_id: int
    sku: str
    price_from: str
    price_to: str
    extension_attributes: dict

    def asdict_by(self, store_view: str) -> dict:
        data = self.asdict()
        if store_view == "all":
            data["store_id"] = 0
        return data
