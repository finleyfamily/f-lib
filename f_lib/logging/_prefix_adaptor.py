"""Logging prefix adaptor."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from ._log_level import LogLevel

if TYPE_CHECKING:
    from collections.abc import Mapping, MutableMapping

    from ._logger import Logger


class PrefixAdaptor(logging.LoggerAdapter["Logger | PrefixAdaptor"]):
    """LoggerAdapter that adds prefixes to messages.

    .. rubric:: Example
    .. code-block:: python

        logger = PrefixAdaptor('something', logging.getLogger('example'))
        logger.info('my message')

    """

    def __init__(
        self,
        prefix: str,
        logger: Logger | PrefixAdaptor,
        *,
        extra: Mapping[str, object] | None = None,
        prefix_template: str = "{prefix}: {msg}",
    ) -> None:
        """Instantiate class.

        Args:
            prefix: Message prefix.
            logger: Logger where the prefixed messages will be sent.
            extra: Mapping of extra values used during message processing.
            prefix_template: String that can be used with
                ``.format(prefix=<prefix>, msg=<msg>)`` to produce a dynamic
                message prefix.

        """
        super().__init__(logger, extra or {})
        self.prefix_template = prefix_template
        self.prefix = prefix

    def notice(
        self,
        msg: Exception | str,
        *,
        exc_info: bool = False,
        extra: Mapping[str, object] | None = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        """Delegate a notice call to the underlying logger.

        Args:
            msg: String template or exception to use for the log record.
            exc_info: Include exception traceback in the log record.
            extra: Dictionary to populated additional information in the log record.
            **kwargs: Arbitrary keyword arguments

        """
        self.log(LogLevel.NOTICE, msg, exc_info=exc_info, extra=extra, **kwargs)

    def process(
        self, msg: object, kwargs: MutableMapping[str, object]
    ) -> tuple[str, MutableMapping[str, object]]:
        """Process the message to append the prefix.

        Args:
            msg: Message to be prefixed.
            kwargs: Keyword args for the message.

        """
        kwargs["extra"] = self.extra
        return self.prefix_template.format(prefix=self.prefix, msg=msg), kwargs

    def success(
        self,
        msg: Exception | str,
        *,
        exc_info: bool = False,
        extra: Mapping[str, object] | None = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        """Delegate a success call to the underlying logger.

        Args:
            msg: String template or exception to use for the log record.
            exc_info: Include exception traceback in the log record.
            extra: Dictionary to populated additional information in the log record.
            **kwargs: Arbitrary keyword arguments

        """
        self.log(LogLevel.SUCCESS, msg, exc_info=exc_info, extra=extra, **kwargs)

    def verbose(
        self,
        msg: Exception | str,
        *,
        exc_info: bool = False,
        extra: Mapping[str, object] | None = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        """Delegate a verbose call to the underlying logger.

        Args:
            msg: String template or exception to use for the log record.
            exc_info: Include exception traceback in the log record.
            extra: Dictionary to populated additional information in the log record.
            **kwargs: Arbitrary keyword arguments

        """
        self.log(LogLevel.VERBOSE, msg, exc_info=exc_info, extra=extra, **kwargs)
