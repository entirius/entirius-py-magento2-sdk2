# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


def dig_categories(categories):
    for category in categories:
        yield category
        if "children_data" in category and category["children_data"]:
            yield from dig_categories(category["children_data"])
