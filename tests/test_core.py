"""Tests standard tap features using the built-in SDK tests library."""

from __future__ import annotations

import datetime as dt

from singer_sdk.testing import SuiteConfig, get_tap_test_class

from tap_readthedocs.tap import TapReadTheDocs

TestTapReadTheDocs = get_tap_test_class(
    TapReadTheDocs,
    config={
        "start_date": (dt.datetime.now(tz=dt.UTC) - dt.timedelta(days=7)).isoformat(),
    },
    suite_config=SuiteConfig(
        max_records_limit=10,
        ignore_no_records_for_streams=[
            "projects",
            "redirects",
            "subprojects",
            "translations",
            "versions",
        ],
    ),
)
