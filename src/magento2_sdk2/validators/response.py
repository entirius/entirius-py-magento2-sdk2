# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
import logging
from json import JSONDecodeError

from requests import Response

logger_process = logging.getLogger("process")


def log_when_fail(response_body, request, code):
    logger_process.error(
        "The magento API responded with an error",
        extra={"details": {"request_params": request.params, "response_body": response_body, "code": code}},
    )


def validate_magento2_response(response: Response, request) -> (bool, dict):
    try:
        response_body = json.loads(response.text)
    except JSONDecodeError:
        body_excerpt = (response.text or "")[:300].replace("\n", " ").strip()
        url = getattr(response, "url", None) or getattr(request, "url", "?")
        content_type = response.headers.get("Content-Type", "?") if response.headers else "?"
        logger_process.error(
            "Magento returned non-JSON response",
            extra={
                "details": {
                    "status_code": response.status_code,
                    "content_type": content_type,
                    "url": url,
                    "body_excerpt": body_excerpt,
                }
            },
        )
        raise ValueError(
            f"Bad response from magento2 (HTTP {response.status_code}, content-type={content_type}): {body_excerpt}"
        )

    if response.status_code == 200:
        return True, response_body

    if response.status_code == 201:
        return True, response_body

    if response.status_code == 202:
        return True, response_body

    if response.status_code == 302:
        return True, response_body

    if response.status_code == 400:
        validation, error_message = validate_magento2_response_body_when_error(response_body)
        if validation:
            log_when_fail(response_body, request, 400)
            raise ValueError(error_message)

    if response.status_code == 401:
        validation, error_message = validate_magento2_response_body_when_error(response_body)
        if validation:
            log_when_fail(response_body, request, 401)
            raise ConnectionError(error_message)

    if response.status_code == 403:
        validation, error_message = validate_magento2_response_body_when_error(response_body)
        if validation:
            log_when_fail(response_body, request, 403)
            raise PermissionError(error_message)

    if response.status_code == 404:
        validation, error_message = validate_magento2_response_body_when_error(response_body)
        if validation:
            log_when_fail(response_body, request, 404)
            raise ValueError(error_message)

    if response.status_code == 408:
        validation, error_message = validate_magento2_response_body_when_error(response_body)
        if validation:
            log_when_fail(response_body, request, 408)
            raise TimeoutError(error_message)

    if response.status_code == 500:
        validation, error_message = validate_magento2_response_body_when_error(response_body)
        if validation:
            log_when_fail(response_body, request, 500)
            raise SystemError(error_message)

    if response.status_code == 503:
        validation, error_message = validate_magento2_response_body_when_error(response_body)
        if validation:
            log_when_fail(response_body, request, 503)
            raise BrokenPipeError(error_message)

    return False, response_body


def get_error_message(body, error_messages):
    if "message" in body:
        error_messages.append(body["message"])
    return error_messages


def validate_magento2_response_body_when_error(response_body: dict) -> (bool, str):
    try:
        error_messages = []
        if "code" in response_body:
            error_messages.append(response_body["code"])

        if "errors" in response_body:
            for each in response_body["errors"]:
                error_messages = get_error_message(each, error_messages)
            return False, " | ".join(error_messages)

        elif "message" in response_body:
            error_messages = get_error_message(response_body, error_messages)
            return True, " | ".join(error_messages)
        else:
            return False, ""
    except Exception as e:
        logger_process.exception(e)
        return True, "Unknown error, check logs for more details."


def validate_magento2_search(response_body: dict) -> (bool, list):
    # full_response_keys = ["items", "aggregations", "search_criteria", "total_count"]
    response_keys = ["items"]
    missing_keys = []
    for key in response_keys:
        if key not in response_body:
            missing_keys.append(key)

    if missing_keys:
        return False, missing_keys
    else:
        return True, []


def validate_magento2_get_customer(response_body: dict) -> (bool, list):
    if response_body.get("items", None) is None:
        return False
    else:
        return True


def validate_magento2_customer_create_batch(response_body: dict) -> (bool, list):
    bulk_uuid = response_body.get("bulk_uuid", None)
    if bulk_uuid:
        return True, response_body
    else:
        return False, []


def validate_magento2_reviews(response_body: dict) -> (bool, list):
    response_keys = ["detail", "id", "title"]
    missing_keys = []
    for key in response_keys:
        if key not in response_body:
            missing_keys.append(key)

    if missing_keys:
        return False, missing_keys
    else:
        return True, []
