"""ReadTheDocs tap class."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from singer_sdk import Tap
from singer_sdk import typing as th

from tap_readthedocs import streams

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

if TYPE_CHECKING:
    from tap_readthedocs.client import ReadTheDocsStream


class TapReadTheDocs(Tap):
    """Singer tap for readthedocs.io."""

    name = "tap-readthedocs"

    config_jsonschema = th.PropertiesList(
        th.Property("token", th.StringType, required=True),
        th.Property(
            "include_business_streams",
            th.BooleanType,
            description=(
                "Whether to include streams available only to ReadTheDocs for Business "
                "accounts."
            ),
            default=False,
        ),
    ).to_dict()

    @override
    def discover_streams(self) -> list[ReadTheDocsStream]:
        result = [
            streams.Builds(tap=self),
            streams.Projects(tap=self),
            streams.Redirects(tap=self),
            streams.Subprojects(tap=self),
            streams.Translations(tap=self),
            streams.Versions(tap=self),
        ]

        if self.config.get("include_business_streams", False):
            result.extend(
                [streams.Organizations(tap=self)],
            )

        return result
