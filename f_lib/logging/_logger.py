"""Custom logger."""

from __future__ import annotations

import logging
from copy import deepcopy
from typing import TYPE_CHECKING, Any, Self, TypeAlias, TypedDict, cast

from ._log_level import LogLevel

if TYPE_CHECKING:
    from collections.abc import Mapping
    from types import TracebackType

_SysExcInfoType: TypeAlias = (
    "tuple[type[BaseException], BaseException, TracebackType | None] | tuple[None, None, None]"
)
_ExcInfoType: TypeAlias = "None | bool | _SysExcInfoType | BaseException"


logging.addLevelName(LogLevel.VERBOSE, LogLevel.VERBOSE.name)
logging.addLevelName(LogLevel.NOTICE, LogLevel.NOTICE.name)
logging.addLevelName(LogLevel.SUCCESS, LogLevel.SUCCESS.name)


class LoggerSettings(TypedDict):
    """Logger settings."""

    markup: bool
    """Enable rich markup (if available)."""


class Logger(logging.Logger):
    """Customized subclass of :class:`logging.Logger`."""

    settings: LoggerSettings
    """Custom logger settings."""

    def __init__(
        self,
        name: str,
        level: LogLevel = LogLevel.NOTSET,
        *,
        markup: bool = False,
    ) -> None:
        """Initialize the logger with a name, level, and settings."""
        super().__init__(name, level)
        self.settings = {"markup": markup}

    def _log(
        self,
        level: int,
        msg: object,
        args: tuple[object, ...] | Mapping[str, object],
        exc_info: _ExcInfoType | None = None,
        extra: Mapping[str, Any] | None = None,
        stack_info: bool = False,  # noqa: FBT001, FBT002
        stacklevel: int = 1,
    ) -> None:
        """Wrap log messages with color."""
        extra = {**deepcopy(extra)} if extra else {}
        if self.settings["markup"]:
            extra.setdefault("markup", self.settings["markup"])
        super()._log(
            level,
            msg,
            args,
            exc_info=exc_info,
            extra=extra,
            stack_info=stack_info,
            stacklevel=stacklevel,
        )

    def notice(
        self,
        msg: Exception | str,
        *,
        exc_info: bool = False,
        extra: Mapping[str, object] | None = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        """Log 'msg % args' with severity ``NOTICE``.

        Args:
            msg: String template or exception to use for the log record.
            exc_info: Include exception traceback in the log record.
            extra: Dictionary to populated additional information in the log record.
            **kwargs: Arbitrary keyword arguments

        """
        if self.isEnabledFor(LogLevel.NOTICE):
            self._log(LogLevel.NOTICE, msg, (), exc_info=exc_info, extra=extra, **kwargs)

    def success(
        self,
        msg: Exception | str,
        *,
        exc_info: bool = False,
        extra: Mapping[str, object] | None = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        """Log 'msg % args' with severity ``SUCCESS``.

        Args:
            msg: String template or exception to use for the log record.
            exc_info: Include exception traceback in the log record.
            extra: Dictionary to populated additional information in the log record.
            **kwargs: Arbitrary keyword arguments

        """
        if self.isEnabledFor(LogLevel.SUCCESS):
            self._log(LogLevel.SUCCESS, msg, (), exc_info=exc_info, extra=extra, **kwargs)

    def verbose(
        self,
        msg: Exception | str,
        *,
        exc_info: bool = False,
        extra: Mapping[str, object] | None = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        """Log 'msg % args' with severity ``VERBOSE``.

        Args:
            msg: String template or exception to use for the log record.
            exc_info: Include exception traceback in the log record.
            extra: Dictionary to populated additional information in the log record.
            **kwargs: Arbitrary keyword arguments

        """
        if self.isEnabledFor(LogLevel.VERBOSE):
            self._log(LogLevel.VERBOSE, msg, (), exc_info=exc_info, extra=extra, **kwargs)

    @classmethod
    def get_logger(cls: type[Self], name: str, *, markup: bool = True) -> Self:
        """Return a logger with the specified name, creating it if necessary.

        This class method replaces :func:`logging.getLogger` to provide the correct logger
        type, only needing to correct it once.
        However, this wrapper requires a name to be provided to avoid use of the root logger.

        .. rubric:: Example
        .. code-block:: python

            LOGGER = Logger.get_logger(__name__)
            LOGGER.info("usage example")

        Args:
            name: Name of the logger. It is recommended to use ``__name__`` here in most cases.
            level: After creating the logger (if needed), set it's level.
            markup: Whether to enable rich markup.

        Returns:
            Custom logger object.

        """
        rv = cast("Self", cls.manager.getLogger(name))
        rv.settings["markup"] = markup
        return rv
