"""Test f_lib.logging._console_handler."""

from __future__ import annotations

import io
import logging
import re
from typing import TYPE_CHECKING, Protocol
from unittest.mock import Mock

import pytest
from rich.console import Console

from f_lib.logging._console_handler import ConsoleHandler
from f_lib.logging._fluid_log_render import FluidLogRender

if TYPE_CHECKING:
    from pytest_mock import MockerFixture

MODULE = "f_lib.logging._console_handler"


def strip_ansi_escape(text: str | bytes) -> str:
    """Remove all ANSI escapes from string or bytes.

    If bytes is passed instead of string, it will be converted to string
    using UTF-8.

    Taken from https://github.com/pycontribs/enrich/blob/6d102221429ee780d7d8185599c02b9a9c11e71d/test/test_logging.py.

    """
    if isinstance(text, bytes):
        text = text.decode("utf-8")

    return re.sub(r"\x1b[^m]*m", "", text)


class TestConsoleHandler:
    """Test ConsoleHandler."""

    def test___init__(self) -> None:
        """Test __init__."""
        obj = ConsoleHandler()
        assert obj.name == "rich.console"
        assert not isinstance(obj._log_render, FluidLogRender)

    def test___init___log_render_kls(self) -> None:
        """Test __init__ with log_render_kls."""
        log_render_kls = Mock(return_value="success")
        obj = ConsoleHandler(log_render_kls=log_render_kls)  # pyright: ignore[reportArgumentType]
        assert obj._log_render == log_render_kls.return_value
        log_render_kls.assert_called_once_with(
            omit_repeated_times=True, show_level=True, show_path=True, show_time=True
        )

    @pytest.mark.parametrize(
        ("escape", "markup", "expected"),
        [(False, False, False), (False, True, False), (True, False, False), (True, True, True)],
    )
    def test__determine_should_escape(self, escape: bool, expected: bool, markup: bool, mocker: MockerFixture) -> None:
        """Test _determine_should_escape."""
        determine_use_markup = mocker.patch.object(ConsoleHandler, "_determine_use_markup", return_value=markup)
        record = Mock(escape=escape)
        assert ConsoleHandler()._determine_should_escape(record) is expected
        determine_use_markup.assert_called_once_with(record)

    @pytest.mark.parametrize(
        ("handler_markup", "record_markup", "expected"),
        [
            (False, False, False),
            (False, True, True),
            (True, False, False),
            (True, True, True),
            (False, None, False),
            (True, None, True),
        ],
    )
    def test__determine_use_markup(self, expected: bool, handler_markup: bool, record_markup: bool | None) -> None:
        """Test _determine_use_markup."""
        record = Mock(markup=record_markup)
        if record_markup is None:
            del record.markup
        assert ConsoleHandler(markup=handler_markup)._determine_use_markup(record) is expected

    def test__style_message(self, mocker: MockerFixture) -> None:
        """Test _style_message."""
        record = Mock()
        determine_use_markup = mocker.patch.object(ConsoleHandler, "_determine_use_markup", return_value=False)
        from_markup = mocker.patch(f"{MODULE}.Text.from_markup")
        assert ConsoleHandler()._style_message(record, "msg") == (record, "msg")
        determine_use_markup.assert_called_once_with(record)
        from_markup.assert_not_called()

    def test__style_message_markup(self, mocker: MockerFixture) -> None:
        """Test _style_message with markup."""
        record = Mock(levelname="INFO")
        determine_use_markup = mocker.patch.object(ConsoleHandler, "_determine_use_markup", return_value=True)
        from_markup = mocker.patch(f"{MODULE}.Text.from_markup", return_value=Mock(markup="success"))
        assert ConsoleHandler()._style_message(record, "msg") == (record, "success")
        determine_use_markup.assert_called_once_with(record)
        from_markup.assert_called_once_with("msg", style="info")

    def test_get_level_text(self, mocker: MockerFixture) -> None:
        """Test get_level_text."""
        record = Mock(levelname="INFO")
        styled = mocker.patch(f"{MODULE}.Text.styled", return_value="styled")
        assert ConsoleHandler().get_level_text(record) == styled.return_value
        styled.assert_called_once_with("[INFO]   ", "logging.level.info")

    def test_render_message(self, mocker: MockerFixture) -> None:
        """Test render_message."""
        record = Mock(name="record")
        determine_should_escape = mocker.patch.object(ConsoleHandler, "_determine_should_escape", return_value=True)
        escape = mocker.patch(f"{MODULE}.escape", return_value="escaped")
        render_message = mocker.patch(f"{MODULE}.RichHandler.render_message", return_value="rendered")
        style_message = mocker.patch.object(ConsoleHandler, "_style_message", return_value=("style", "message"))
        assert ConsoleHandler().render_message(record, "message") == render_message.return_value
        determine_should_escape.assert_called_once_with(record)
        escape.assert_called_once_with("message")
        style_message.assert_called_once_with(record, "escaped")
        render_message.assert_called_once_with("style", "message")


class SetupLoggingProtocol(Protocol):  # noqa: D101
    def __call__(  # noqa: D102
        self, *, show_level: bool, show_path: bool, show_time: bool
    ) -> tuple[logging.Logger, ConsoleHandler]: ...


@pytest.fixture(name="rich_logger")
def rich_logger_fixture() -> SetupLoggingProtocol:
    """Returns tuple with logger and handler to be tested.

    Taken from https://github.com/pycontribs/enrich/blob/6d102221429ee780d7d8185599c02b9a9c11e71d/test/test_logging.py.

    """

    def _setup_logging(*, show_level: bool, show_path: bool, show_time: bool) -> tuple[logging.Logger, ConsoleHandler]:
        rich_handler = ConsoleHandler(
            console=Console(
                file=io.StringIO(),
                force_terminal=True,
                width=80,
                color_system="truecolor",
                soft_wrap=True,
            ),
            log_render_kls=FluidLogRender,
            enable_link_path=False,
            show_level=show_level,
            show_path=show_path,
            show_time=show_time,
        )

        logging.basicConfig(level="NOTSET", format="%(message)s", datefmt="[DATE]", handlers=[rich_handler])
        rich_log = logging.getLogger("rich")
        rich_log.addHandler(rich_handler)
        return (rich_log, rich_handler)

    return _setup_logging


@pytest.mark.parametrize("show_level", [False, True])
@pytest.mark.parametrize("show_path", [False, True])
@pytest.mark.parametrize("show_time", [False, True])
def test_logging(
    rich_logger: SetupLoggingProtocol,
    show_level: bool,
    show_path: bool,
    show_time: bool,
) -> None:
    """Test that logger does not wrap.

    Taken from https://github.com/pycontribs/enrich/blob/6d102221429ee780d7d8185599c02b9a9c11e71d/test/test_logging.py.

    """
    (logger, rich_handler) = rich_logger(show_level=show_level, show_path=show_path, show_time=show_time)
    date_str = rich_handler.console.get_datetime().date().strftime("%x")
    file_name = __file__.split("/")[-1]

    text = 10 * "x"  # a long text that would likely wrap on a normal console
    logger.error("%s %s", text, 123)

    # verify that the long text was not wrapped
    output = strip_ansi_escape(
        rich_handler.console.file.getvalue()  # pyright: ignore[reportAttributeAccessIssue, reportUnknownArgumentType]
    )
    assert text in output
    assert "\n" not in output[:-1]

    if show_level:
        assert "ERROR" in output
    else:
        assert "ERROR" not in output

    if show_path:
        assert file_name in output
    else:
        assert file_name not in output

    if show_time:
        assert date_str in output
    else:
        assert date_str not in output
