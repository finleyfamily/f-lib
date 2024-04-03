"""Console logging settings."""

from __future__ import annotations

from pydantic import BaseModel


class ConsoleLoggingSettings(BaseModel):
    """Console logging settings."""

    enable_markup: bool = True
    """Enable `rich <https://github.com/Textualize/rich>`__ markup in console logs."""

    enable_rich_tracebacks: bool = True
    """Enable using `rich <https://github.com/Textualize/rich>`__ to highlight tracebacks."""

    log_format: str | None = None
    """Custom log format to use instead of using default formats."""

    show_level: bool = True
    """Show a column for the level of each log message."""

    show_path: bool = False
    """Show the path to the original log call."""

    show_time: bool = False
    """Show a column for time with the log messages."""

    time_format: str = "[%x %X]"
    """Format to use when showing the time column.

    :attr:`~f_lib.logging.settings.ConsoleLoggingConfig.show_time` must be enabled
    for this to take effect.

    """

    tracebacks_show_locals: bool = True
    """Show local variables in trackbacks."""

    tracebacks_theme: str = "one-dark"
    """Theme from `pygments <https://pygments.org/>`__ to use when highlighting tracebacks."""
