"""Tests for client-side incremental filtering of the builds stream."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any
from unittest.mock import patch

from singer_sdk import RESTStream

from tap_readthedocs.streams import Builds
from tap_readthedocs.tap import TapReadTheDocs

if TYPE_CHECKING:
    from collections.abc import Iterator

CUTOFF = datetime(2024, 1, 2, tzinfo=UTC)


def _records(*created: str, seen: list[str]) -> Iterator[dict[str, Any]]:
    for c in created:
        seen.append(c)
        yield {"created": c}


def _sync(cutoff: datetime | None, *created: str) -> tuple[list[str], list[str]]:
    """Return (emitted, consumed) created timestamps."""
    seen: list[str] = []
    stream = Builds(TapReadTheDocs(config={"token": "x"}, parse_env_config=False))
    with (
        patch.object(Builds, "get_starting_timestamp", return_value=cutoff),
        patch.object(
            RESTStream,
            "request_records",
            return_value=_records(*created, seen=seen),
        ),
    ):
        emitted = [r["created"] for r in stream.request_records(None)]
    return emitted, seen


def test_stops_at_bookmark() -> None:
    """Older records are dropped and the upstream generator is not drained."""
    emitted, seen = _sync(
        CUTOFF,
        "2024-01-04T00:00:00Z",
        "2024-01-02T00:00:00Z",  # at the bookmark: kept
        "2024-01-01T00:00:00Z",  # older: stop here
        "2023-12-31T00:00:00Z",
    )
    assert emitted == ["2024-01-04T00:00:00Z", "2024-01-02T00:00:00Z"]
    assert seen == [*emitted, "2024-01-01T00:00:00Z"]


def test_no_bookmark_emits_everything() -> None:
    """Without state, all records are emitted."""
    created = ["2024-01-04T00:00:00Z", "2020-01-01T00:00:00Z"]
    emitted, _ = _sync(None, *created)
    assert emitted == created
