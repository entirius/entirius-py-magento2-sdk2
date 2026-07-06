# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import ClassVar

from marshmallow import Schema
from marshmallow_dataclass import add_schema, dataclass


@add_schema
@dataclass
class ReviewRatesPayload:
    rating_name: str
    value: str
    Schema: ClassVar[type[Schema]] = Schema


@add_schema
@dataclass
class ReviewDetailsPayload:
    title: str
    detail: str
    nickname: str
    ratings: list[ReviewRatesPayload] | None
    review_entity: str
    review_status: int
    entity_pk_value: int
    uuid: str | None
    Schema: ClassVar[type[Schema]] = Schema


@dataclass
class ReviewPayload:
    review: ReviewDetailsPayload
