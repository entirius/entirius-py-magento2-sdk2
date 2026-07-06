# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import builtins
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any, ClassVar

from marshmallow import Schema
from marshmallow_dataclass import add_schema

from magento2_sdk2.dto import DTO


@dataclass
class Filter:
    class ConditionType:
        EqualValue = "eq"
        NotEqualValue = "neq"
        LikeValue = "like"
        NotLikeValue = "nlike"
        IsValue = "is"
        InValues = "in"
        NotInValues = "nin"
        ValueIsNotNull = "notnull"
        ValueIsNull = "null"
        MoreOrEqualValue = "moreq"
        GreaterValue = "gt"
        LessValue = "lt"
        GreaterOrEqualValue = "gteq"
        LessOrEqualValue = "lteq"
        ValueInSet = "finset"
        FromValue = "from"
        ToValue = "to"

    field: str
    value: str
    condition_type: str = ""


@dataclass
class FilterGroup:
    filters: Sequence[Filter]


@dataclass
class SuggestParameters:
    q: str = None


@dataclass
class BaseParams(DTO):
    page_size: int = field(default=12)
    current_page: int = field(default=0)
    filter_groups: Sequence[FilterGroup] = field(default_factory=list)
    request_params: dict = field(default_factory=dict)

    def create_type_search_parameters(self, is_advanced_searcher: bool = False):
        """Creates param which specify type of search"""
        if is_advanced_searcher:
            self.request_params["searchCriteria[requestName]"] = "advanced_search_container"
        else:
            self.request_params["searchCriteria[requestName]"] = "quick_search_container"

    def create_field_parameter(self, value):
        """Creates param which specify fields in reposonse  ex.fields=items[id]"""
        self.request_params["fields"] = value

    def create_page_parameters(self):
        """Creates params which specify which page and size page"""
        self.request_params["searchCriteria[page_size]"] = self.page_size
        self.request_params["searchCriteria[current_page]"] = self.current_page

    def create_filter_parameters(self):
        """Creates params which limiting request"""
        if self.filter_groups:
            for idx_group, filter_group in enumerate(self.filter_groups):
                for idx_filter, each in enumerate(filter_group.filters):
                    self.request_params[f"searchCriteria[filterGroups][{idx_group}][filters][{idx_filter}][value]"] = (
                        each.value
                    )
                    self.request_params[f"searchCriteria[filterGroups][{idx_group}][filters][{idx_filter}][field]"] = (
                        each.field
                    )
                    self.request_params[
                        f"searchCriteria[filterGroups][{idx_group}][filters][{idx_filter}][conditionType]"
                    ] = each.condition_type


@dataclass
class SearchParameters(BaseParams):
    search_text: str = None
    price_from: int = None
    price_to: int = None
    sku: str = None
    category_ids: str = None
    visibility: str = None
    Schema: ClassVar[type[Schema]] = Schema

    def create_filters(self):
        all_filters = [
            Filter(field="search_term", value=self.search_text),
            Filter(field="price.from", value=self.price_from),
            Filter(field="price.to", value=self.price_to),
            Filter(field="sku", value=self.sku),
            Filter(field="category_ids", value=self.category_ids),
            Filter(field="visibility", value=self.visibility),
        ]
        filters = [each for each in all_filters if each.value is not None]
        self.filter_groups = [FilterGroup(filters=filters)]


@add_schema
@dataclass
class SearchResult:
    title: str | None = None
    num_results: str | None = None
    type: str | None = None
    image: str | None = None
    url: str | None = None
    price: str | None = None
    sku: str | None = None
    breadcrumb: Any | None = None
    Schema: ClassVar[builtins.type[Schema]] = Schema

    def get_only_important_data(self, suggest_data, text_search):
        match self.type:
            case "product":
                suggest_data["sku"].append(self.sku)
                return suggest_data
            case "term":
                if self.title != text_search:
                    suggest_data["term"].append({"suggestion": self.title})
                return suggest_data
            case _:
                return suggest_data
