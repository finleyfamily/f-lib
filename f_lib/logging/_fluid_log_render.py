"""Adapted from https://github.com/pycontribs/enrich/blob/v1.2.7/src/enrich/logging.py."""

from __future__ import annotations

from typing import TYPE_CHECKING

from rich.text import Text, TextType

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable
    from datetime import datetime

    from rich.console import Console, ConsoleRenderable


class FluidLogRender:
    """Renders log by not using a table and avoiding any wrapping."""

    def __init__(
        self,
        *,
        show_time: bool = True,
        show_level: bool = False,
        show_path: bool = True,
        time_format: str | Callable[[datetime], Text] = "[%x %X]",
        omit_repeated_times: bool = True,
        level_width: int | None = 8,
    ) -> None:
        """Instantiate class."""
        self.show_time = show_time
        self.show_level = show_level
        self.show_path = show_path
        self.time_format = time_format
        self.omit_repeated_times = omit_repeated_times
        self.level_width = level_width
        self._last_time: Text | None = None

    def __call__(
        self,
        console: Console,
        renderables: Iterable[ConsoleRenderable],
        log_time: datetime | None = None,
        time_format: str | Callable[[datetime], Text] | None = None,
        level: TextType = "",
        path: str | None = None,
        line_no: int | None = None,
        link_path: str | None = None,
    ) -> Text:
        result = Text()
        if self.show_time:
            if log_time is None:  # cov: ignore
                log_time = console.get_datetime()
            time_format = time_format or self.time_format
            log_time_display = (
                time_format(log_time)
                if callable(time_format)
                else Text(log_time.strftime(time_format))
            )
            if log_time_display == self._last_time and self.omit_repeated_times:
                result += Text(" " * len(log_time_display))
            else:
                result += log_time_display
                self._last_time = log_time_display

        if self.show_level:
            if not isinstance(level, Text):  # cov: ignore
                level = Text(level)
            # CRITICAL is the longest identifier from default set.
            if len(level) < 9:  # cov: ignore
                level += " " * (9 - len(level))
            result += level

        for elem in renderables:
            result += elem

        if self.show_path and path:
            path_text = Text(" ", style="repr.filename")
            path_text.append(path, style=f"link file://{link_path}" if link_path else "")
            if line_no:
                path_text.append(f":{line_no}")
            result += path_text

        return result
