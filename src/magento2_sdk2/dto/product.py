# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from dataclasses import dataclass, field
from decimal import Decimal

from magento2_sdk2.dto import DTO


class ProductType:
    SIMPLE = "simple"
    CONFIGURABLE = "configurable"
    VIRTUAL = "virtual"
    DOWNLOADABLE = "downloadable"
    BUNDLE = "bundle"
    GROUPED = "grouped"


class ProductVisibility:
    NOT_VISIBLE_INDIVIDUALLY = 1
    CATALOG = 2
    SEARCH = 3
    CATALOG_AND_SEARCH = 4


class ProductExtensionAttributes:
    BUNDLE_PRODUCT_OPTIONS = "bundle_product_options"
    CATEGORY_LINKS = "category_links"
    CONFIGURABLE_PRODUCT_LINKS = "configurable_product_links"
    CONFIGURABLE_PRODUCT_OPTIONS = "configurable_product_options"
    DISCOUNTS = "discounts"
    DOWNLOADABLE_PRODUCT_LINKS = "downloadable_product_links"
    DOWNLOADABLE_PRODUCT_SAMPLES = "downloadable_product_samples"
    GIFTCARD_AMOUNTS = "giftcard_amounts"
    STOCK_ITEM = "stock_item"
    WEBSITE_IDS = "website_ids"


@dataclass
class CustomAttribute(DTO):
    attribute_code: str
    value: any


@dataclass
class ProductLink(DTO):
    id: str
    sku: str
    option_id: int
    qty: int
    position: int
    is_default: bool
    price: Decimal
    price_type: int
    can_change_quantity: int


@dataclass
class BundleProductOption(DTO):
    option_id: int
    title: str
    required: bool
    type: str
    position: int
    sku: str
    product_links: list[ProductLink]


@dataclass
class ConfigurableProductOptionValue(DTO):
    value_index: int  # magento attribute.pk


@dataclass
class ConfigurableProductOption(DTO):
    id: int
    attribute_id: str  # magento feature.pk
    label: str
    position: int
    product_id: int  # magento product.pk
    values: list[ConfigurableProductOptionValue]


@dataclass
class ProductLite(DTO):
    sku: str
    custom_attributes: list[CustomAttribute]
    status: int


@dataclass
class ProductPrice(DTO):
    sku: str
    price: Decimal


@dataclass
class Product(DTO):
    # nie robie całego odwzorowania produktu bo nie potrzebuje na razie
    locale: str
    id: int
    sku: str
    name: str
    attribute_set_id: int
    status: int
    visibility: int
    type_id: str
    extension_attributes: dict
    custom_attributes: list[CustomAttribute]
    price: Decimal
    # date format 0000-00-00 00:00:00
    created_at: str
    updated_at: str
    weight: int = 0
    price: Decimal | None

    def asdict_for_create(self) -> dict:
        data = self.asdict()
        data.pop("locale")
        data.pop("id")
        return data

    @staticmethod
    def factory(data: dict, locale: str) -> "Product":
        custom_attributes = []
        for custom_attribute in data.get("custom_attributes", []):
            ca = CustomAttribute(**custom_attribute)
            custom_attributes.append(ca)

        extension_attributes = {}
        ext_attrs_raw = data.get("extension_attributes", {})

        if isinstance(ext_attrs_raw, list):
            ext_attrs_raw = {}

        for key, value in ext_attrs_raw.items():
            match key:
                case ProductExtensionAttributes.BUNDLE_PRODUCT_OPTIONS:
                    bundle_options_list = []
                    for bundle_product_option in value:
                        product_links = []
                        if "product_links" in bundle_product_option:
                            for product_link in bundle_product_option["product_links"]:
                                product_link = ProductLink(**product_link)
                                product_links.append(product_link)
                        bundle_product_option.pop("product_links")
                        bundle_product_option = BundleProductOption(
                            **bundle_product_option, product_links=product_links
                        )
                        bundle_options_list.append(bundle_product_option)
                    extension_attributes[key] = bundle_options_list
                case ProductExtensionAttributes.CONFIGURABLE_PRODUCT_OPTIONS:
                    configurable_options_list = []
                    for configurable_product_option in value:
                        configurable_values = []
                        if "values" in configurable_product_option:
                            for configurable_value in configurable_product_option["values"]:
                                configurable_value = ConfigurableProductOptionValue(**configurable_value)
                                configurable_values.append(configurable_value)
                        configurable_product_option.pop("values")
                        configurable_product_option = ConfigurableProductOption(
                            **configurable_product_option, values=configurable_values
                        )
                        configurable_options_list.append(configurable_product_option)
                    extension_attributes[key] = configurable_options_list
                case _:
                    extension_attributes[key] = value

        return Product(
            locale=locale,
            id=data["id"],
            sku=data["sku"],
            name=data["name"],
            attribute_set_id=data["attribute_set_id"],
            status=data["status"],
            visibility=data["visibility"],
            type_id=data["type_id"],
            extension_attributes=extension_attributes,
            custom_attributes=custom_attributes,
            price=Decimal(data.get("price", 0)),
            weight=data.get("weight", 0),
            created_at=data["created_at"],
            updated_at=data["updated_at"],
        )


@dataclass
class ProductLocale(DTO):
    # Obiekt który zawiera wszystkie lokalizacje w jednym miejscu
    id: int
    sku: str
    name: dict[str, str]
    price: Decimal | None
    attribute_set_id: int
    status: int
    visibility: int
    type_id: str
    extension_attributes: dict
    custom_attributes: dict[str, list[CustomAttribute]]
    bundle_option_titles_t9n: dict[str, dict[str, str]] = field(default_factory=dict)

    @staticmethod
    def factory(products: list[Product]) -> "ProductLocale":
        product = None
        for p in products:
            if not product:
                product = ProductLocale(
                    id=p.id,
                    sku=p.sku,
                    price=p.price,
                    name={p.locale: p.name},
                    attribute_set_id=p.attribute_set_id,
                    status=p.status,
                    visibility=p.visibility,
                    type_id=p.type_id,
                    extension_attributes=p.extension_attributes,
                    custom_attributes={p.locale: p.custom_attributes},
                )
            else:
                product.custom_attributes[p.locale] = p.custom_attributes
                product.name[p.locale] = p.name
            ProductLocale._collect_bundle_option_titles(product.bundle_option_titles_t9n, p)
        return product

    @staticmethod
    def _collect_bundle_option_titles(target: dict[str, dict[str, str]], p: "Product") -> None:
        bundle_options = p.extension_attributes.get(ProductExtensionAttributes.BUNDLE_PRODUCT_OPTIONS, [])
        for option in bundle_options:
            title = getattr(option, "title", None)
            if not title:
                continue
            for link in getattr(option, "product_links", []):
                target.setdefault(link.sku, {})[p.locale] = title
