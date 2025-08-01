"""Test f_lib.logging.utils."""

from __future__ import annotations

import logging
import logging.handlers
import secrets
import string
from typing import TYPE_CHECKING
from unittest.mock import Mock

import pytest

from f_lib.logging import ConsoleHandler
from f_lib.logging.utils import (
    find_handler,
    is_stream_handler,
    optionally_replace_handler,
    walk_propagation_tree,
)

if TYPE_CHECKING:
    from pytest_mock import MockerFixture

MODULE = "f_lib.logging.utils"


@pytest.fixture
def root_logger() -> logging.Logger:
    """Root logger."""
    return logging.getLogger()


@pytest.fixture
def parent_logger(root_logger: logging.Logger) -> logging.Logger:
    """Parent logger."""
    return root_logger.getChild("".join(secrets.choice(string.digits + string.ascii_letters) for _ in range(8)))


@pytest.fixture
def child_logger(parent_logger: logging.Logger) -> logging.Logger:
    """Child logger."""
    return parent_logger.getChild("child")


@pytest.fixture
def grandchild_logger(child_logger: logging.Logger) -> logging.Logger:
    """Grandchild logger."""
    return child_logger.getChild("grand")


@pytest.mark.parametrize("expected_handler", [logging.StreamHandler(), ConsoleHandler()])
def test_find_handler(
    child_logger: logging.Logger,
    expected_handler: logging.Handler,
    grandchild_logger: logging.Logger,
    parent_logger: logging.Logger,
) -> None:
    """Test find_handler."""
    syslog_handler = logging.handlers.SysLogHandler()
    child_logger.addHandler(expected_handler)
    parent_logger.addHandler(syslog_handler)
    matched_handler, matched_logger = find_handler(grandchild_logger)
    assert matched_handler is expected_handler
    assert matched_logger is child_logger


def test_find_handler_none(grandchild_logger: logging.Logger) -> None:
    """Test find_handler."""
    matched_handler, matched_logger = find_handler(grandchild_logger)
    assert matched_handler is None
    assert matched_logger is None


@pytest.mark.parametrize(
    ("handler", "expected"),
    [
        (ConsoleHandler(), True),
        (logging.StreamHandler(), True),
        (logging.handlers.SysLogHandler(), False),
    ],
)
def test_is_stream_handler(expected: bool, handler: logging.Handler) -> None:
    """Test is_stream_handler."""
    assert is_stream_handler(handler) is expected


@pytest.mark.parametrize("reconfigure", [False, True])
def test_optionally_replace_handler(mocker: MockerFixture, reconfigure: bool) -> None:
    """Test optionally_replace_handler."""
    handler = Mock(name="handler")
    logger, other_logger = Mock(name="logger"), Mock(name="other_logger")
    match_handler = Mock(name="match_handler")
    find_handler = mocker.patch(f"{MODULE}.find_handler", return_value=(handler, other_logger))

    result = optionally_replace_handler(logger, match_handler=match_handler, reconfigure=reconfigure)
    find_handler.assert_called_once_with(logger, match_handler)
    if reconfigure:
        other_logger.removeHandler.assert_called_once_with(handler)
        assert result == (handler, other_logger)
    else:
        other_logger.removeHandler.assert_not_called()
        assert result == (handler, logger)


@pytest.mark.parametrize("reconfigure", [False, True])
def test_optionally_replace_handler_no_handler(mocker: MockerFixture, reconfigure: bool) -> None:
    """Test optionally_replace_handler no handler."""
    logger = Mock(name="logger")
    find_handler = mocker.patch(f"{MODULE}.find_handler", return_value=(None, None))
    assert optionally_replace_handler(logger, reconfigure=reconfigure) == (None, logger)
    find_handler.assert_called_once_with(logger, is_stream_handler)


def test_walk_propagation_tree(
    child_logger: logging.Logger,
    grandchild_logger: logging.Logger,
    parent_logger: logging.Logger,
    root_logger: logging.Logger,
) -> None:
    """Test walk_propagation_tree."""
    assert list(walk_propagation_tree(grandchild_logger)) == [
        grandchild_logger,
        child_logger,
        parent_logger,
        root_logger,
    ]


def test_walk_propagation_tree_no_propagate(child_logger: logging.Logger, grandchild_logger: logging.Logger) -> None:
    """Test walk_propagation_tree."""
    child_logger.propagate = False
    assert list(walk_propagation_tree(grandchild_logger)) == [
        grandchild_logger,
        child_logger,
    ]
