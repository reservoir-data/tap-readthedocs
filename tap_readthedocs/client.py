"""REST client handling, including ReadTheDocsStream base class."""

from __future__ import annotations

import sys
from http import HTTPStatus
from typing import TYPE_CHECKING, Any, TypeVar

import requests_cache
from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.pagination import BaseOffsetPaginator
from singer_sdk.streams import RESTStream

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

if TYPE_CHECKING:
    from singer_sdk.helpers.types import Context

requests_cache.install_cache()
TStream = TypeVar("TStream", bound=RESTStream[int])


class ReadTheDocsStream(RESTStream[int]):
    """ReadTheDocs stream class."""

    url_base = "https://readthedocs.org"
    records_jsonpath = "$.results[*]"
    page_size = 50
    extra_retry_statuses = (HTTPStatus.TOO_MANY_REQUESTS,)

    @property
    @override
    def authenticator(self) -> APIKeyAuthenticator:
        return APIKeyAuthenticator(
            key="Authorization",
            value="Token {token}".format(**self.config),
            location="header",
        )

    @override
    def get_url_params(
        self,
        context: Context | None,
        next_page_token: int | None,
    ) -> dict[str, Any]:
        return {
            "limit": self.page_size,
            "offset": next_page_token,
            "expand": "config",
        }

    @override
    def get_new_paginator(self) -> BaseOffsetPaginator:
        return BaseOffsetPaginator(start_value=0, page_size=self.page_size)
