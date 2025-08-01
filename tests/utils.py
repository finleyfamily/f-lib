"""Utilities for testing."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from pathlib import Path

    import pytest

ArchiveFixtureLiteral = Literal["bz2_file", "gz_file", "gzip_file", "tar_file", "xz_file", "zip_file"]


def get_archive_fixture(
    request: pytest.FixtureRequest,
    fixture_name: ArchiveFixtureLiteral,
) -> Path:
    """Get archive fixture dynamically (e.g. in a parametrized test)."""
    return request.getfixturevalue(fixture_name)
