"""Helper function to setup logging."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from ._console_handler import ConsoleHandler
from ._constants import DEFAULT_LOG_FORMAT
from .settings import LoggingSettings
from .utils import optionally_replace_handler

if TYPE_CHECKING:
    from collections.abc import Iterable
    from types import ModuleType

    from rich.console import Console
    from rich.highlighter import Highlighter

    from ._log_level import LogLevel


def setup_logging(
    *,
    console: Console,
    formatter: logging.Formatter | None = None,
    handler_kls: type[ConsoleHandler] | None = None,
    highlighter: Highlighter | None = None,
    level: LogLevel | None = None,
    logger: logging.Logger,
    reconfigure: bool = False,
    settings: LoggingSettings | None = None,
    tracebacks_suppress: Iterable[ModuleType | str] = ("click",),
) -> None:
    """Set up :mod:`rich` logging.

    This function is similar in purpose to :func:`logging.basicConfig`.
    Both setup logging with a lot of optional keyword arguments with logical
    defaults that *should* cover most needs.

    When using this function, **DO NOT** add any other handlers to a :class:`~logging.Logger`
    that would propagate to what is passed to this function.
    Doing so will result in duplicate log statements.
    This is intended to be the **last** or **only** step when setting up logging
    (other than setting levels).

    Args:
        console: :class:`~rich.console.Console` to log to.
        formatter: :class:`logging.Formatter` to add to the :class:`logging.Handler`.
        handler_kls: Override the handler class to use.
        highlighter: Optional :class:`~rich.highlighter.Highlighter` to use.
            If not provided, :mod:`rich's <rich>` default :class:`~rich.highlighter.Highlighter`
            is used.
        level: :class:`~f_lib.logging.LogLevel` to set.
        logger: Instance of the :class:`~f_lib.logging.Logger` to setup.
        reconfigure: Replace previous log configuration if found.
        settings: :class:`~f_lib.logging.settings.LoggingSettings` object.
        tracebacks_suppress: List of tracebacks to suppress.

    """
    handler_kls = ConsoleHandler if handler_kls is None else handler_kls
    settings = settings if settings else LoggingSettings()
    if level:
        logger.setLevel(level)
    handler, logger = optionally_replace_handler(logger, reconfigure=reconfigure)
    if not (handler and not reconfigure):
        filters = handler.filters if handler else None
        handler = handler_kls(
            console=console,
            highlighter=highlighter,
            log_time_format=settings.console.time_format,
            markup=settings.console.enable_markup,
            rich_tracebacks=settings.console.enable_rich_tracebacks,
            show_level=settings.console.show_level,
            show_path=settings.console.show_path,
            show_time=settings.console.show_time,
            tracebacks_show_locals=settings.console.tracebacks_show_locals,
            tracebacks_suppress=tracebacks_suppress,
            tracebacks_theme=settings.console.tracebacks_theme,
        )
        if filters:
            handler.filters = filters
        handler.setFormatter(
            formatter if formatter is not None else logging.Formatter(DEFAULT_LOG_FORMAT)
        )
        logger.addHandler(handler)
