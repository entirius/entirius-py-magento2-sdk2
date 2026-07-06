# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from dataclasses import dataclass

from magento2_sdk2.dto import DTO


@dataclass
class AttributeSet(DTO):
    """
    Represents Magento 2 Attribute Set.

    Attributes:
        attribute_set_id: Unique identifier of the attribute set
        attribute_set_name: Name of the attribute set
        sort_order: Sort order for display
        entity_type_id: Entity type (4 for products)
    """

    attribute_set_id: int
    attribute_set_name: str
    sort_order: int
    entity_type_id: int
