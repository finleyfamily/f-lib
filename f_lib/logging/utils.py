"""Logging utilities."""

from __future__ import annotations

import logging
import sys
from typing import TYPE_CHECKING, TextIO, TypeVar

from rich.logging import RichHandler

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable, Iterator


LoggerTypeVar = TypeVar("LoggerTypeVar", bound=logging.Logger)


def is_stream_handler(handler: logging.Handler, streams: Iterable[TextIO] | None = None) -> bool:
    """Whether a stream handlers writing to the given streams(s).

    Args:
        handler: The :class:`logging.Handler` to check.
        streams: An array of streams to match against.

    """
    streams = streams or (sys.stderr, sys.stdout)
    return isinstance(handler, RichHandler) or (
        isinstance(handler, logging.StreamHandler) and handler.stream in streams
    )


def find_handler(
    logger: LoggerTypeVar,
    match_handler: Callable[[logging.Handler], bool] = is_stream_handler,
) -> tuple[logging.Handler, LoggerTypeVar] | tuple[None, None]:
    """Find :class:`logging.Handler`(s) in the propagation tree of a :class:`~logging.Logger`.

    This function finds a :class:`logging.Handler` attached to a logger or one of
    it's parents (see :func:`walk_propagation_tree()`).

    Args:
        logger: The :class:`~logging.Logger` to check.
        match_handler: A callable that receives a :class:`~logging.Handler`
            object and returns :data:`True` to match a handler or :data:`False`
            to skip that handler and continue searching for a match.

    Returns:
        A tuple of two values:

            1. The matched :class:`~logging.Handler` object or :data:`None`
                if no handler was matched.
            2. The :class:`~logging.Logger` object to which the handler is
                attached or :data:`None` if no handler was matched.

    """
    for log in walk_propagation_tree(logger):
        if hasattr(log, "handlers"):
            for handler in log.handlers:
                if match_handler(handler):
                    return handler, log
    return None, None


def optionally_replace_handler(
    logger: LoggerTypeVar,
    *,
    match_handler: Callable[[logging.Handler], bool] = is_stream_handler,
    reconfigure: bool = False,
) -> tuple[logging.Handler | None, LoggerTypeVar]:
    """Prepare to replace a handler if needed and configured to do so.

    Args:
        logger: The :class:`~logging.Logger` to optionally replace the handler for.
        match_handler: A callable that receives a :class:`~logging.Handler`
            object and returns :data:`True` to match a handler or :data:`False`
            to skip that handler and continue searching for a match.
        reconfigure: Whether to replace an existing :class:`~logging.Handler`.

    Returns:
        A tuple of two values:

            1. The matched :class:`~logging.Handler` object or :data:`None`
                if no handler was matched.
            2. The :class:`~logging.Logger` to which the matched handler was
                attached or the logger given to :func:`replace_handler()`.

    """
    handler, other_logger = find_handler(logger, match_handler)
    if handler and other_logger and reconfigure:
        other_logger.removeHandler(handler)
        logger = other_logger
    return handler, logger


def walk_propagation_tree(
    logger: LoggerTypeVar | None,
) -> Iterator[LoggerTypeVar]:
    """Walk through the propagation hierarchy of the given logger.

    Args:
        logger: The logger whose hierarchy to walk (a :class:`~logging.Logger` object).

    Yields:
        :class:`~logging.Logger` objects.

    """
    while logger is not None:
        yield logger
        logger = logger.parent if logger.propagate and hasattr(logger, "parent") else None
