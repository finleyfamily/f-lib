"""Test f_lib.logging._setup_logging."""

from __future__ import annotations

import logging
import secrets
import string
from typing import TYPE_CHECKING
from unittest.mock import Mock

import pytest

from f_lib.logging._log_level import LogLevel
from f_lib.logging._setup_logging import DEFAULT_LOG_FORMAT, setup_logging
from f_lib.logging.settings import LoggingSettings

if TYPE_CHECKING:
    from pytest_mock import MockerFixture


MODULE = "f_lib.logging._setup_logging"


@pytest.fixture(autouse=True)
def formatter(mocker: MockerFixture) -> Mock:
    """Patch out ``logging.Formatter``."""
    return mocker.patch(
        f"{MODULE}.logging.Formatter",
        return_value=logging.Formatter(logging.BASIC_FORMAT),
    )


@pytest.fixture(autouse=True)
def handler_kls(mocker: MockerFixture) -> Mock:
    """Patch out ``ConsoleHandler``."""
    return mocker.patch(f"{MODULE}.ConsoleHandler", return_value=logging.StreamHandler())


@pytest.fixture
def logger() -> logging.Logger:
    """Logger."""
    return logging.getLogger("".join(secrets.choice(string.digits + string.ascii_letters) for _ in range(8)))


@pytest.fixture
def optionally_replace_handler(mocker: MockerFixture, logger: logging.Logger) -> Mock:
    """Patch optionally_replace_handler."""
    return mocker.patch(f"{MODULE}.optionally_replace_handler", return_value=(None, logger))


@pytest.fixture(autouse=True)
def set_level(mocker: MockerFixture) -> Mock:
    """Patch ``setLevel`` of logger."""
    return mocker.patch.object(logging.Logger, "setLevel", return_value=None)


def test_setup_logging(
    formatter: Mock,
    handler_kls: Mock,
    logger: logging.Logger,
    mocker: MockerFixture,
    optionally_replace_handler: Mock,
    set_level: Mock,
) -> None:
    """Test setup_logging using all default settings."""
    console, settings = Mock(), LoggingSettings()
    settings_kls = mocker.patch(f"{MODULE}.LoggingSettings", return_value=settings)
    assert not setup_logging(console=console, logger=logger)
    settings_kls.assert_called_once_with()
    set_level.assert_not_called()
    optionally_replace_handler.assert_called_once_with(logger, reconfigure=False)
    handler_kls.assert_called_once_with(
        console=console,
        highlighter=None,
        log_time_format=settings.console.time_format,
        markup=settings.console.enable_markup,
        rich_tracebacks=settings.console.enable_rich_tracebacks,
        show_level=settings.console.show_level,
        show_path=settings.console.show_path,
        show_time=settings.console.show_time,
        tracebacks_show_locals=settings.console.tracebacks_show_locals,
        tracebacks_suppress=("click",),
        tracebacks_theme=settings.console.tracebacks_theme,
    )
    formatter.assert_called_once_with(DEFAULT_LOG_FORMAT)
    assert handler_kls.return_value.formatter == formatter.return_value, (
        "setFormatter should be called to add a formatter to the handler"
    )
    assert logger.handlers == [handler_kls.return_value], "addHandler should be called to add the handler to the logger"


def test_setup_logging_no_reconfigure(
    handler_kls: Mock,
    logger: logging.Logger,
    optionally_replace_handler: Mock,
) -> None:
    """Test setup_logging no reconfigure."""
    handler = Mock(name="handler")
    optionally_replace_handler.return_value = (handler, logger)
    assert not setup_logging(console=Mock(), logger=logger, reconfigure=False)
    handler_kls.assert_not_called()


def test_setup_logging_reconfigure(
    handler_kls: Mock,
    logger: logging.Logger,
    optionally_replace_handler: Mock,
) -> None:
    """Test setup_logging reconfigure."""
    handler = Mock(name="handler", filters=[Mock(name="filter0"), Mock(name="filter1")])
    optionally_replace_handler.return_value = (handler, logger)
    assert not setup_logging(
        console=Mock(),
        logger=logger,
        handler_kls=handler_kls,  # pyright: ignore[reportArgumentType]
        reconfigure=True,
    )
    optionally_replace_handler.assert_called_once_with(logger, reconfigure=True)
    assert handler_kls.return_value.filters == handler.filters
    assert logger.handlers == [handler_kls.return_value], "addHandler should be called to add the handler to the logger"


@pytest.mark.parametrize("reconfigure", [False, True])
def test_setup_logging_user_provided(
    handler_kls: Mock,
    logger: logging.Logger,
    mocker: MockerFixture,
    optionally_replace_handler: Mock,
    reconfigure: bool,
    set_level: Mock,
) -> None:
    """Test setup_logging with user provided values."""
    console, highlighter = Mock(name="console"), Mock(name="highlighter")
    settings = LoggingSettings()
    custom_formatter = logging.Formatter(DEFAULT_LOG_FORMAT)
    settings_kls = mocker.patch(f"{MODULE}.LoggingSettings", return_value=settings)
    assert not setup_logging(
        console=console,
        formatter=custom_formatter,
        highlighter=highlighter,
        level=LogLevel.INFO,
        logger=logger,
        reconfigure=reconfigure,
        settings=settings,
        tracebacks_suppress=("foo",),
    )
    settings_kls.assert_not_called()
    set_level.assert_called_once_with(LogLevel.INFO)
    optionally_replace_handler.assert_called_once_with(logger, reconfigure=reconfigure)
    handler_kls.assert_called_once_with(
        console=console,
        highlighter=highlighter,
        log_time_format=settings.console.time_format,
        markup=settings.console.enable_markup,
        rich_tracebacks=settings.console.enable_rich_tracebacks,
        show_level=settings.console.show_level,
        show_path=settings.console.show_path,
        show_time=settings.console.show_time,
        tracebacks_show_locals=settings.console.tracebacks_show_locals,
        tracebacks_suppress=("foo",),
        tracebacks_theme=settings.console.tracebacks_theme,
    )
    assert handler_kls.return_value.formatter == custom_formatter, (
        "setFormatter should be called to add a formatter to the handler"
    )
    assert logger.handlers == [handler_kls.return_value], "addHandler should be called to add the handler to the logger"
