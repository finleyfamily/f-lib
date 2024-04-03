"""Log level enum."""

from __future__ import annotations

from enum import IntEnum


class LogLevel(IntEnum):
    """Log level enum."""

    NOTSET = 0  # same as logging.NOTSET
    """When set on a logger, indicates that ancestor loggers are to be consulted
    to determine the effective level.

    If that still resolves to NOTSET, then all events are logged. When set on a
    handler, all events are handled.

    """

    SPAM = 5
    """Custom level for spam messages."""

    DEBUG = 10  # same as logging.DEBUG
    """Detailed information, typically only of interest to a developer trying to diagnose a problem."""

    VERBOSE = 15
    """Custom level between INFO and DEBUG.

    Useful where some additional information might be desirable but does not cause
    full information dumps everywhere.

    """

    INFO = 20  # same as logging.INFO
    """Confirmation that things are working as expected.

    This is the *default* level most things will want to set at.

    """

    NOTICE = 25
    """Custom level situated between INFO and WARNING to draw attention without raising concern."""

    WARNING = 30  # same as logging.WARNING
    """An indication that something unexpected happened, or that a problem might
    occur in the near future (e.g. disk space low).

    The software is still working as expected.

    """

    SUCCESS = 35
    """Custom log level used when something good happens."""

    ERROR = 40  # same as logging.ERROR
    """Due to a more serious problem, the software has not been able to perform some function."""

    CRITICAL = 50  # same as logging.CRITICAL | logging.FATAL
    """A serious error, indicating that the program itself may be unable to continue running."""

    FATAL = 50  # same as logging.CRITICAL | logging.FATAL
    """A serious error, indicating that the program itself may be unable to continue running."""

    @classmethod
    def from_verbosity(cls, verbosity: int) -> LogLevel:
        """Determine appropriate log level from verbosity.

        +-----------+----------------------------------------+
        | Verbosity | Log Level                              |
        +===========+========================================+
        | ``0``     | :attr:`f_lib.logging.LogLevel.FATAL`   |
        +-----------+----------------------------------------+
        | ``1``     | :attr:`f_lib.logging.LogLevel.INFO`    |
        +-----------+----------------------------------------+
        | ``2``     | :attr:`f_lib.logging.LogLevel.VERBOSE` |
        +-----------+----------------------------------------+
        | ``3``     | :attr:`f_lib.logging.LogLevel.DEBUG`   |
        +-----------+----------------------------------------+
        | ``4``     | :attr:`f_lib.logging.LogLevel.DEBUG`   |
        +-----------+----------------------------------------+
        | ``5`` +   | :attr:`f_lib.logging.LogLevel.NOTSET`  |
        +-----------+----------------------------------------+

        Args:
            verbosity: Requested level of verbosity.

        Returns:
            A log level based on the table above.

        """
        if not verbosity:
            return cls.FATAL
        if verbosity == 1:
            return cls.INFO
        if verbosity == 2:
            return cls.VERBOSE
        if verbosity < 5:
            return cls.DEBUG
        return cls.NOTSET

    @classmethod
    def has_value(cls, value: int) -> bool:
        """Check if :class:`f_lib.logging.LogLevel` has a value."""
        return value in cls._value2member_map_
