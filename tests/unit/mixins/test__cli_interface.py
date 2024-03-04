"""Test f_lib.mixins._cli_interface."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import TYPE_CHECKING, Any
from unittest.mock import Mock

import pytest

from f_lib.mixins._cli_interface import CliInterfaceMixin

if TYPE_CHECKING:
    from pytest_mock import MockerFixture
    from pytest_subprocess import FakeProcess

    from f_lib import Environment

MODULE = "f_lib.mixins._cli_interface"


class TestCliInterfaceMixin:
    """Test CliInterfaceMixin."""

    class Kls(CliInterfaceMixin):
        """Used in tests."""

        def __init__(self, cwd: Path, environment: Environment) -> None:
            """Instantiate class."""
            self.cwd = cwd
            self.env = environment

    @pytest.mark.parametrize("env", [None, {"foo": "bar"}])
    def test__run_command(
        self, env: dict[str, str] | None, mocker: MockerFixture, tmp_path: Path
    ) -> None:
        """Test _run_command."""
        ctx_env = {"foo": "bar", "bar": "foo"}
        mock_subprocess = mocker.patch(f"{MODULE}.subprocess.check_output", return_value="success")
        assert (
            self.Kls(tmp_path, Mock(vars=ctx_env))._run_command("test", env=env)
            == mock_subprocess.return_value
        )
        mock_subprocess.assert_called_once_with(
            "test",
            cwd=tmp_path,
            env=env or ctx_env,
            shell=True,
            stderr=subprocess.STDOUT,
            text=True,
        )

    def test__run_command_capture_output(
        self,
        environment: Environment,
        fake_process: FakeProcess,
        tmp_path: Path,
    ) -> None:
        """Test _run_command with capture_output."""
        fake_process.register_subprocess(
            "test",
            returncode=0,
            stdout="\x1b[33msuccess\x1b[39m",  # cspell: disable-line
        )
        assert (
            self.Kls(tmp_path, environment)._run_command(
                "test", suppress_output=False, capture_output=True
            )
            == "success"
        )

    def test__run_command_capture_output_called_process_error(
        self,
        environment: Environment,
        fake_process: FakeProcess,
        tmp_path: Path,
    ) -> None:
        """Test _run_command with capture_output."""
        fake_process.register_subprocess(
            "test", returncode=1, stdout="\x1b[33mfail\x1b[39m"  # cspell: disable-line
        )
        with pytest.raises(subprocess.CalledProcessError) as excinfo:
            self.Kls(tmp_path, environment)._run_command(
                "test", suppress_output=False, capture_output=True
            )
        assert excinfo.value.returncode == 1
        assert excinfo.value.output == "fail"

    def test__run_command_no_suppress_output(self, mocker: MockerFixture, tmp_path: Path) -> None:
        """Test _run_command."""
        env = {"foo": "bar"}
        mock_convert_list_to_shell_str = mocker.patch(
            f"{MODULE}.convert_list_to_shell_str", return_value="success"
        )
        mock_subprocess = mocker.patch(f"{MODULE}.subprocess.check_call", return_value=0)
        assert not self.Kls(tmp_path, Mock(vars=env))._run_command(
            ["foo", "bar"], suppress_output=False
        )
        mock_convert_list_to_shell_str.assert_called_once_with(["foo", "bar"])
        mock_subprocess.assert_called_once_with(
            mock_convert_list_to_shell_str.return_value,
            cwd=tmp_path,
            env=env,
            shell=True,
        )

    @pytest.mark.parametrize("return_value", [False, True])
    def test_found_in_path(self, mocker: MockerFixture, return_value: bool) -> None:
        """Test found_in_path."""
        exe = mocker.patch.object(self.Kls, "EXECUTABLE", "foo.exe", create=True)
        mock_which = Mock(return_value=return_value)
        mocker.patch(f"{MODULE}.shutil", which=mock_which)
        assert self.Kls.found_in_path() is return_value
        mock_which.assert_called_once_with(exe)

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
    def test_generate_command(
        self,
        expected: list[str],
        mocker: MockerFixture,
        provided: dict[str, Any],
    ) -> None:
        """Test generate_command."""
        exe = mocker.patch.object(self.Kls, "EXECUTABLE", "test.exe", create=True)
        assert self.Kls.generate_command("command", **provided) == [
            exe,
            "command",
            *expected,
        ]

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
    def test_generate_command_list(
        self,
        expected: list[str],
        mocker: MockerFixture,
        provided: dict[str, Any],
    ) -> None:
        """Test generate_command."""
        exe = mocker.patch.object(self.Kls, "EXECUTABLE", "test.exe", create=True)
        assert self.Kls.generate_command(["command", "arg"], **provided) == [
            exe,
            "command",
            "arg",
            *expected,
        ]

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
    def test_generate_command_none(
        self,
        expected: list[str],
        mocker: MockerFixture,
        provided: dict[str, Any],
    ) -> None:
        """Test generate_command."""
        exe = mocker.patch.object(self.Kls, "EXECUTABLE", "test.exe", create=True)
        assert self.Kls.generate_command(**provided) == [
            exe,
            *expected,
        ]
