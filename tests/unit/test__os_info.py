"""Test f_lib._os_info."""

# ruff: noqa: ARG002
from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import Mock

import pytest

from f_lib._os_info import OsInfo

if TYPE_CHECKING:
    from pathlib import Path

    from pytest_mock import MockerFixture

MODULE = "f_lib._os_info"


@pytest.fixture()
def clear_os_info() -> None:
    """Clear OsInfo singleton."""
    OsInfo.clear_singleton()


@pytest.mark.usefixtures("clear_os_info")
class TestOsInfo:
    """Test OsInfo."""

    def test___platform_dirs_darwin(self, mocker: MockerFixture, platform_darwin: None) -> None:
        """Test _platform_dirs macOS."""
        mock_unix = mocker.patch(f"{MODULE}.Unix", return_value="success")
        mock_windows = mocker.patch(f"{MODULE}.Windows")

        assert OsInfo()._platform_dirs == mock_unix.return_value
        mock_windows.assert_not_called()
        mock_unix.assert_called_once_with(appname="f-lib", appauthor="finley")

    def test___platform_dirs_linux(self, mocker: MockerFixture, platform_linux: None) -> None:
        """Test _platform_dirs Linux."""
        mock_unix = mocker.patch(f"{MODULE}.Unix", return_value="success")
        mock_windows = mocker.patch(f"{MODULE}.Windows")

        assert OsInfo()._platform_dirs == mock_unix.return_value
        mock_windows.assert_not_called()
        mock_unix.assert_called_once_with(appname="f-lib", appauthor="finley")

    def test___platform_dirs_windows(self, mocker: MockerFixture, platform_windows: None) -> None:
        """Test _platform_dirs Windows."""
        mock_unix = mocker.patch(f"{MODULE}.Unix")
        mock_windows = mocker.patch(f"{MODULE}.Windows", return_value="success")

        assert OsInfo()._platform_dirs == mock_windows.return_value
        mock_windows.assert_called_once_with(appname="f-lib", appauthor="finley")
        mock_unix.assert_not_called()

    def test_is_darwin_false(self, platform_linux: None) -> None:
        """Test is_darwin False."""
        assert not OsInfo().is_darwin

    def test_is_darwin(self, platform_darwin: None) -> None:
        """Test is_darwin."""
        assert OsInfo().is_darwin

    def test_is_linux_false(self, platform_darwin: None) -> None:
        """Test is_linux False."""
        assert not OsInfo().is_linux

    def test_is_linux(self, platform_linux: None) -> None:
        """Test is_linux."""
        assert OsInfo().is_linux

    def test_is_macos_false(self, platform_linux: None) -> None:
        """Test is_macos False."""
        assert not OsInfo().is_macos

    def test_is_macos(self, platform_darwin: None) -> None:
        """Test is_macos."""
        assert OsInfo().is_macos

    def test_is_posix_false(self, mocker: MockerFixture) -> None:
        """Test is_posix False."""
        mock_os = mocker.patch(f"{MODULE}.os")
        mock_os.name = "nt"
        assert not OsInfo().is_posix

    def test_is_posix(self, mocker: MockerFixture) -> None:
        """Test is_posix."""
        mock_os = mocker.patch(f"{MODULE}.os")
        mock_os.name = "posix"
        assert OsInfo().is_posix

    def test_is_windows_false(self, platform_linux: None) -> None:
        """Test is_windows False."""
        assert not OsInfo().is_windows

    def test_is_windows(self, platform_windows: None) -> None:
        """Test is_windows."""
        assert OsInfo().is_windows

    def test_name_darwin(self, platform_darwin: None) -> None:
        """Test name darwin."""
        assert OsInfo().name == "darwin"

    def test_name_linux(self, platform_linux: None) -> None:
        """Test name linux."""
        assert OsInfo().name == "linux"

    def test_name_windows(self, platform_windows: None) -> None:
        """Test name windows."""
        assert OsInfo().name == "windows"

    def test_singleton(self) -> None:
        """Test singleton."""
        assert id(OsInfo()) == id(OsInfo())

    def test_user_config_dir(self, mocker: MockerFixture, tmp_path: Path) -> None:
        """Test user_config_dir."""
        mocker.patch.object(OsInfo, "_platform_dirs", Mock(user_config_dir=tmp_path))
        assert OsInfo().user_config_dir == tmp_path

    def test_user_data_dir(self, mocker: MockerFixture, tmp_path: Path) -> None:
        """Test user_data_dir."""
        mocker.patch.object(OsInfo, "_platform_dirs", Mock(user_data_dir=tmp_path))
        assert OsInfo().user_data_dir == tmp_path
