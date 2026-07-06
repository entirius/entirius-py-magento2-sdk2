# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from dataclasses import dataclass, field


@dataclass
class CustomerData:
    email: str
    firstname: str | None = ""
    lastname: str | None = ""
    store_id: int | None = None
    addresses: list[dict] | None = field(default_factory=list)


@dataclass
class MainCustomerData:
    customer: CustomerData


@dataclass
class Address:
    defaultShipping: bool | None
    defaultBilling: bool | None
    firstname: str | None
    lastname: str | None
    region: dict | None
    postcode: str | None
    street: list[str] | None
    city: str | None
    telephone: str | None
    countryId: str | None


@dataclass
class RequestItem:
    id: int
    data_hash: str
    status: str


@dataclass
class ApiResponse:
    bulk_uuid: str
    request_items: list[RequestItem]
    errors: bool
