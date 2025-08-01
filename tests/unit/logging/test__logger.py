"""Test f_lib.logging._logger."""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import Mock

import pytest

from f_lib.logging._log_level import LogLevel
from f_lib.logging._logger import Logger, LoggerSettings

if TYPE_CHECKING:
    from pytest_mock import MockerFixture


@pytest.fixture
def is_enabled_for(mocker: MockerFixture) -> Mock:
    """Mock Logger.isEnabledFor with ``return_value=True``."""
    return mocker.patch.object(Logger, "isEnabledFor", return_value=True)


@pytest.fixture
def log(mocker: MockerFixture) -> Mock:
    """Mock Logger._log."""
    return mocker.patch.object(Logger, "_log")


class TestLogger:
    """Test Logger."""

    def test__log(self, mocker: MockerFixture) -> None:
        """Test _log."""
        mock_log = mocker.patch("f_lib.logging._logger.logging.Logger._log")
        assert not Logger("test")._log(LogLevel.INFO, "this is a test", (), extra={"key": "val"})
        mock_log.assert_called_once_with(
            LogLevel.INFO,
            "this is a test",
            (),
            exc_info=None,
            extra={"key": "val", "markup": False},
            stack_info=False,
            stacklevel=2,
        )

    def test__log_markup(self, mocker: MockerFixture) -> None:
        """Test _log markup."""
        mock_log = mocker.patch("f_lib.logging._logger.logging.Logger._log")
        assert not Logger("test", settings=LoggerSettings(markup=True))._log(LogLevel.INFO, "this is a test", ())
        mock_log.assert_called_once_with(
            LogLevel.INFO,
            "this is a test",
            (),
            exc_info=None,
            extra={"markup": True},
            stack_info=False,
            stacklevel=2,
        )

    def test_get_logger(self, mocker: MockerFixture) -> None:
        """Test get_logger."""
        result = Mock(name="success", settings=LoggerSettings(markup=False))
        get_logger = mocker.patch.object(Logger.manager, "getLogger", return_value=result)
        assert Logger.get_logger("foo") == result
        get_logger.assert_called_once_with("foo")
        assert result.setting.markup

    @pytest.mark.parametrize("enabled", [False, True])
    def test_notice(self, enabled: bool, is_enabled_for: Mock, log: Mock) -> None:
        """Test notice."""
        is_enabled_for.return_value = enabled
        assert not Logger("test").notice("msg", key="val")
        is_enabled_for.assert_called_once_with(LogLevel.NOTICE)
        if enabled:
            log.assert_called_once_with(LogLevel.NOTICE, "msg", (), exc_info=False, extra=None, key="val")
        else:
            log.assert_not_called()

    @pytest.mark.parametrize("enabled", [False, True])
    def test_success(self, enabled: bool, is_enabled_for: Mock, log: Mock) -> None:
        """Test success."""
        is_enabled_for.return_value = enabled
        assert not Logger("test").success("msg", key="val")
        is_enabled_for.assert_called_once_with(LogLevel.SUCCESS)
        if enabled:
            log.assert_called_once_with(LogLevel.SUCCESS, "msg", (), exc_info=False, extra=None, key="val")
        else:
            log.assert_not_called()

    @pytest.mark.parametrize("enabled", [False, True])
    def test_verbose(self, enabled: bool, is_enabled_for: Mock, log: Mock) -> None:
        """Test verbose."""
        is_enabled_for.return_value = enabled
        assert not Logger("test").verbose("msg", key="val")
        is_enabled_for.assert_called_once_with(LogLevel.VERBOSE)
        if enabled:
            log.assert_called_once_with(LogLevel.VERBOSE, "msg", (), exc_info=False, extra=None, key="val")
        else:
            log.assert_not_called()
