"""Test f_lib.utils.__init__."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

import pytest

from f_lib.utils import (
    convert_kwargs_to_shell_list,
    convert_list_to_shell_str,
    convert_to_cli_flag,
)

if TYPE_CHECKING:
    from pytest_mock import MockerFixture

MODULE = "f_lib.utils"


@pytest.mark.parametrize(
    ("provided", "expected"),
    [
        ({}, []),
        ({"is_flag": True}, ["--is-flag"]),
        ({"is_flag": False}, []),
        ({"key": "val", "is-flag": True}, ["--key", "val", "--is-flag"]),
        ({"user": ["foo", "bar"]}, ["--user", "foo", "--user", "bar"]),
        (
            {"file": [Path("/tmp/foo"), Path("/tmp/bar")]},
            ["--file", "/tmp/foo", "--file", "/tmp/bar"],
        ),
    ],
)
def test_convert_kwargs_to_shell_list(
    expected: list[str], provided: dict[str, Any]
) -> None:
    """Test convert_kwargs_to_shell_list."""
    assert convert_kwargs_to_shell_list(**provided) == expected


@pytest.mark.parametrize("platform", ["Darwin", "Linux"])
def test_convert_list_to_shell_str(mocker: MockerFixture, platform: str) -> None:
    """Test convert_list_to_shell_str."""
    mock_list2cmdline = mocker.patch(f"{MODULE}.subprocess.list2cmdline")
    mocker.patch("platform.system", return_value=platform)
    mock_join = mocker.patch("shlex.join", return_value="success")
    assert convert_list_to_shell_str("foo") == mock_join.return_value
    mock_list2cmdline.assert_not_called()
    mock_join.assert_called_once_with("foo")


def test_convert_list_to_shell_str_windows(mocker: MockerFixture) -> None:
    """Test convert_list_to_shell_str on Windows systems."""
    mock_list2cmdline = mocker.patch(
        f"{MODULE}.subprocess.list2cmdline", return_value="success"
    )
    mocker.patch("platform.system", return_value="Windows")
    mock_join = mocker.patch("shlex.join")
    assert convert_list_to_shell_str("foo") == mock_list2cmdline.return_value
    mock_list2cmdline.assert_called_once_with("foo")
    mock_join.assert_not_called()


@pytest.mark.parametrize(
    ("prefix", "provided", "expected"),
    [
        (None, "foo", "--foo"),
        ("-", "foo_bar", "-foo-bar"),
        ("--", "foo-bar", "--foo-bar"),
    ],
)
def test_convert_to_cli_flag(expected: str, prefix: str | None, provided: str) -> None:
    """Test convert_to_cli_flag."""
    if prefix:
        assert convert_to_cli_flag(provided, prefix=prefix) == expected
    else:
        assert convert_to_cli_flag(provided) == expected
