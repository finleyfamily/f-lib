"""Logging constants."""

from __future__ import annotations

from typing import TYPE_CHECKING

from rich.style import Style

if TYPE_CHECKING:
    from collections.abc import Mapping

DEFAULT_LOG_FORMAT = "%(message)s"
"""Default log format."""

DEFAULT_LOG_FORMAT_VERBOSE = "%(name)s: %(message)s"
"""Default log format when a verbose log level is used."""

DEFAULT_STYLES: Mapping[str, Style] = {
    "error": Style(color="red"),
    "info": Style(),
    "notice": Style(color="yellow"),
    "success": Style(color="green"),
    "warning": Style(color="orange1"),
    "logging.level.critical": Style(color="red", bold=True, reverse=True),
    "logging.level.debug": Style(color="green"),
    "logging.level.error": Style(color="red", bold=True),
    "logging.level.info": Style(color="blue"),
    "logging.level.notice": Style(color="yellow"),
    "logging.level.notset": Style(dim=True),
    "logging.level.spam": Style(color="green", dim=True),
    "logging.level.success": Style(color="green", bold=True),
    "logging.level.verbose": Style(color="cyan"),
    "logging.level.warning": Style(color="orange1"),
    "logging.keyword": Style(bold=True, color="blue"),
    "repr.brace": Style(),
    "repr.call": Style(),
    "repr.ellipsis": Style(dim=True, italic=True),
}
"""Default :class:`rich.style.Style` overrides."""
