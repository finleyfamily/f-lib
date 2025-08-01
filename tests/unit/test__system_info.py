"""Test f_lib._system_info."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from f_lib._os_info import OsInfo
from f_lib._system_info import SystemInfo, UnknownPlatformArchitectureError

if TYPE_CHECKING:
    from pytest_mock import MockerFixture

MODULE = "f_lib._system_info"


@pytest.fixture
def clear_system_info() -> None:
    """Clear OsInfo singleton."""
    SystemInfo.clear_singleton()


@pytest.mark.usefixtures("clear_system_info")
class TestSystemInfo:
    """Test SystemInfo."""

    def test___bool__(self) -> None:
        """Test __bool__."""
        assert SystemInfo()

    def test___eq__(self) -> None:
        """Test __eq__."""
        assert SystemInfo() == SystemInfo()

    def test___eq___false(self) -> None:
        """Test __eq__ is ``False``."""
        assert not SystemInfo() == OsInfo()  # noqa: SIM201

    def test___hash__(self) -> None:
        """Test __hash__."""
        obj = SystemInfo()
        assert isinstance(hash(obj), int)

        # Ensure that the hash is consistent
        assert hash(obj) == hash(obj)

    def test___nq__(self) -> None:
        """Test __ne__."""
        assert SystemInfo() != OsInfo()

    def test___ne___false(self) -> None:
        """Test __ne__ is ``False``."""
        assert not SystemInfo() != SystemInfo()  # noqa: SIM202

    @pytest.mark.parametrize(
        ("expected", "is_64bit", "is_arm", "is_x86"),
        [
            ("amd32", False, False, True),
            ("amd64", True, False, True),
            ("arm32", False, True, False),
            ("arm64", True, True, False),
        ],
    )
    def test_architecture(
        self,
        expected: str,
        is_64bit: bool,
        is_arm: bool,
        is_x86: bool,
        mocker: MockerFixture,
    ) -> None:
        """Test architecture."""
        mocker.patch.object(SystemInfo, "is_64bit", is_64bit)
        mocker.patch.object(SystemInfo, "is_arm", is_arm)
        mocker.patch.object(SystemInfo, "is_x86", is_x86)
        assert SystemInfo().architecture == expected

    def test_architecture_unknown(self, mocker: MockerFixture) -> None:
        """Test architecture."""
        mocker.patch.object(SystemInfo, "is_64bit", False)
        mocker.patch.object(SystemInfo, "is_arm", False)
        mocker.patch.object(SystemInfo, "is_x86", False)
        with pytest.raises(UnknownPlatformArchitectureError):
            SystemInfo().architecture  # noqa: B018

    @pytest.mark.parametrize(("expected", "maxsize"), [(False, 2**33), (True, 2**32)])
    def test_is_32bit(self, expected: bool, maxsize: int, mocker: MockerFixture) -> None:
        """Test is_32bit."""
        mocker.patch(f"{MODULE}.sys.maxsize", maxsize)
        assert SystemInfo().is_32bit is expected

    @pytest.mark.parametrize(("expected", "maxsize"), [(False, 2**32), (True, 2**33)])
    def test_is_64bit(self, expected: bool, maxsize: int, mocker: MockerFixture) -> None:
        """Test is_64bit."""
        mocker.patch(f"{MODULE}.sys.maxsize", maxsize)
        assert SystemInfo().is_64bit is expected

    @pytest.mark.parametrize(("expected", "machine"), [(False, "leg"), (True, "arm"), (True, "ARM"), (True, "aarch")])
    def test_is_arm(self, expected: bool, machine: str, mocker: MockerFixture) -> None:
        """Test is_arm."""
        platform_machine = mocker.patch(f"{MODULE}.platform.machine", return_value=machine)
        assert SystemInfo().is_arm is expected
        platform_machine.assert_called_once_with()

    def test_is_frozen_false(self) -> None:
        """Test is_frozen False."""
        assert not SystemInfo().is_frozen

    def test_is_frozen(self, mocker: MockerFixture) -> None:
        """Test is_frozen."""
        mocker.patch(f"{MODULE}.sys.frozen", True, create=True)
        assert SystemInfo().is_frozen

    def test_os(self) -> None:
        """Test os."""
        assert isinstance(SystemInfo().os, OsInfo)

    def test_singleton(self) -> None:
        """Test singleton."""
        assert id(SystemInfo()) == id(SystemInfo())

    @pytest.mark.parametrize(
        ("expected", "machine"),
        [(False, "arm"), (True, "AMD64"), (True, "i386"), (True, "x86_64")],
    )
    def test_is_x86(self, expected: bool, machine: str, mocker: MockerFixture) -> None:
        """Test is_x86."""
        platform_machine = mocker.patch(f"{MODULE}.platform.machine", return_value=machine)
        assert SystemInfo().is_x86 is expected
        platform_machine.assert_called_once_with()
