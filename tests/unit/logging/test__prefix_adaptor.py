"""Test f_lib.logging._prefix_adaptor."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from f_lib.logging._log_level import LogLevel
from f_lib.logging._logger import Logger
from f_lib.logging._prefix_adaptor import PrefixAdaptor

if TYPE_CHECKING:
    from unittest.mock import Mock

    from pytest_mock import MockerFixture

LOGGER = Logger(__name__)


@pytest.fixture()
def log(mocker: MockerFixture) -> Mock:
    """Mock PrefixAdaptor.log."""
    return mocker.patch.object(PrefixAdaptor, "log")


class TestPrefixAdaptor:
    """Test PrefixAdaptor."""

    def test___init__(self) -> None:
        """Test __init__."""
        obj = PrefixAdaptor("test_init", LOGGER)
        assert obj.prefix == "test_init"
        assert obj.prefix_template == "{prefix}: {msg}"

    def test_notice(self, log: Mock) -> None:
        """Test notice."""
        assert not PrefixAdaptor("test", LOGGER).notice("msg", key="val")
        log.assert_called_once_with(LogLevel.NOTICE, "msg", exc_info=False, extra=None, key="val")

    def test_process(self) -> None:
        """Test process."""
        assert PrefixAdaptor("test_process", LOGGER, extra={"foo": "bar"}).process(
            "msg", {"kwargs": "value"}
        ) == ("test_process: msg", {"extra": {"foo": "bar"}, "kwargs": "value"})

    def test_success(self, log: Mock) -> None:
        """Test success."""
        assert not PrefixAdaptor("test_success", LOGGER).success("msg", key="val")
        log.assert_called_once_with(LogLevel.SUCCESS, "msg", exc_info=False, extra=None, key="val")

    def test_verbose(self, log: Mock) -> None:
        """Test verbose."""
        assert not PrefixAdaptor("test_verbose", LOGGER).verbose("msg", key="val")
        log.assert_called_once_with(LogLevel.VERBOSE, "msg", exc_info=False, extra=None, key="val")
