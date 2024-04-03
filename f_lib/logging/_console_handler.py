"""Custom console :class:`~rich.logging.RichHandler`."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from rich.logging import RichHandler
from rich.markup import escape
from rich.text import Text

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable
    from datetime import datetime
    from types import ModuleType

    from rich.console import Console, ConsoleRenderable
    from rich.highlighter import Highlighter

    from ._fluid_log_render import FluidLogRender


class ConsoleHandler(RichHandler):
    """Custom console :class:`~rich.logging.RichHandler`."""

    def __init__(  # noqa: PLR0913
        self,
        level: int | str = logging.NOTSET,
        console: Console | None = None,
        *,
        enable_link_path: bool = True,
        highlighter: Highlighter | None = None,
        keywords: list[str] | None = None,
        locals_max_length: int = 10,
        locals_max_string: int = 80,
        log_render_kls: type[FluidLogRender] | None = None,
        log_time_format: str | Callable[[datetime], Text] = "[%x %X]",
        markup: bool = False,
        name: str = "rich.console",
        omit_repeated_times: bool = True,
        rich_tracebacks: bool = False,
        show_level: bool = True,
        show_path: bool = True,
        show_time: bool = True,
        tracebacks_extra_lines: int = 3,
        tracebacks_show_locals: bool = False,
        tracebacks_suppress: Iterable[str | ModuleType] = (),
        tracebacks_theme: str | None = None,
        tracebacks_width: int | None = None,
        tracebacks_word_wrap: bool = True,
        **kwargs: object,
    ) -> None:
        """Instantiate class.

        Args:
            level: Log level.
            console: Optional console instance to write logs.
                Default will use a global console instance writing to stdout.
            enable_link_path: Enable terminal link of path column to file.
            highlighter: Highlighter to style log messages, or None to use ReprHighlighter.
            keywords: List of words to highlight instead of ``RichHandler.KEYWORDS``.
            locals_max_length: Maximum length of containers before abbreviating, or None for no abbreviation.
            locals_max_string: Maximum length of string before truncating, or None to disable.
            log_render_kls: Custom log rendering class.
                If not provided, will use the one provided by rich.
            log_time_format: If ``log_time`` is enabled, either string for strftime or callable that formats the time.
            markup: Enable console markup in log messages.
            name: Name of the handler. Can be used to check for existence.
            omit_repeated_times: Omit repetition of the same time.
            rich_tracebacks: Enable rich tracebacks with syntax highlighting and formatting.
            show_level: Show a column for the level.
            show_path: Show the path to the original log call.
            show_time: Show a column for the time.
            tracebacks_extra_lines: Additional lines of code to render tracebacks, or None for full width.
            tracebacks_show_locals: Enable display of locals in tracebacks.
            tracebacks_suppress: Optional sequence of modules or paths to exclude from traceback.
            tracebacks_theme: Override pygments theme used in traceback.
            tracebacks_width: Number of characters used to render tracebacks, or None for full width.
            tracebacks_word_wrap: Enable word wrapping of long tracebacks lines.
            **kwargs: Additional options added to :class:`~rich.logging.RichHandler`
                that are not explicitly listed here. This is to provide support for future
                releases without requiring a new release here to support it.

        """
        super().__init__(
            level,
            console,
            enable_link_path=enable_link_path,
            highlighter=highlighter,
            keywords=keywords,
            locals_max_length=locals_max_length,
            locals_max_string=locals_max_string,
            log_time_format=log_time_format,
            markup=markup,
            omit_repeated_times=omit_repeated_times,
            rich_tracebacks=rich_tracebacks,
            show_level=show_level,
            show_path=show_path,
            show_time=show_time,
            tracebacks_extra_lines=tracebacks_extra_lines,
            tracebacks_show_locals=tracebacks_show_locals,
            tracebacks_suppress=tracebacks_suppress,
            tracebacks_theme=tracebacks_theme,
            tracebacks_width=tracebacks_width,
            tracebacks_word_wrap=tracebacks_word_wrap,
            **kwargs,
        )
        if log_render_kls is not None:
            self._log_render = log_render_kls(
                omit_repeated_times=omit_repeated_times,
                show_level=show_level,
                show_path=show_path,
                show_time=show_time,
            )
        self._name = name

    def _determine_should_escape(self, record: logging.LogRecord) -> bool:
        """Determine if a log message should be passed to :function:`~rich.markup.escape`.

        This can be overridden in subclasses for more control.

        """
        return self._determine_use_markup(record) and getattr(record, "escape", False)

    def _determine_use_markup(self, record: logging.LogRecord) -> bool:
        """Determine if markup should be used for a log record."""
        return getattr(record, "markup", self.markup)

    def render_message(self, record: logging.LogRecord, message: str) -> ConsoleRenderable:
        """Render message text in to Text.

        Args:
            record: logging Record.
            message: String containing log message.

        Returns:
            ConsoleRenderable: Renderable to display log message.

        """
        if self._determine_should_escape(record):
            message = escape(message)
        return super().render_message(*self._style_message(record, message))

    def _style_message(
        self,
        record: logging.LogRecord,
        message: str,
    ) -> tuple[logging.LogRecord, str]:
        """Apply style to the message."""
        if not self._determine_use_markup(record):
            return record, message
        return record, Text.from_markup(message, style=record.levelname.lower()).markup

    def get_level_text(self, record: logging.LogRecord) -> Text:
        """Get the level name from the record.

        Args:
            record: LogRecord instance.

        Returns:
            Text: A tuple of the style and level name.

        """
        level_name = record.levelname
        return Text.styled(f"[{level_name}]".ljust(9), f"logging.level.{level_name.lower()}")
