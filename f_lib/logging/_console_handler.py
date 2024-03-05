"""Custom console :class:`~rich.logging.RichHandler`."""

from __future__ import annotations

from typing import TYPE_CHECKING

from rich.logging import RichHandler
from rich.markup import escape
from rich.text import Text

if TYPE_CHECKING:
    import logging

    from rich.console import ConsoleRenderable


class ConsoleHandler(RichHandler):
    """Custom console :class:`~rich.logging.RichHandler`."""

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
