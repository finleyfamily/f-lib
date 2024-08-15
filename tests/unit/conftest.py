"""Pytest configuration, fixtures, and plugins."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from f_lib import Environment

if TYPE_CHECKING:
    from pathlib import Path

    from pytest_mock import MockerFixture


@pytest.fixture
def environment(tmp_path: Path) -> Environment:
    """Create a deploy environment that can be used for testing."""
    return Environment(root_dir=tmp_path)


@pytest.fixture
def platform_darwin(mocker: MockerFixture) -> None:
    """Patch platform.system to always return "Darwin"."""
    mocker.patch("platform.system", return_value="Darwin")


@pytest.fixture
def platform_linux(mocker: MockerFixture) -> None:
    """Patch platform.system to always return "Linux"."""
    mocker.patch("platform.system", return_value="Linux")


@pytest.fixture
def platform_windows(mocker: MockerFixture) -> None:
    """Patch platform.system to always return "Windows"."""
    mocker.patch("platform.system", return_value="Windows")
