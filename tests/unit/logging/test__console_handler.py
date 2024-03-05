"""Test f_lib.logging._console_handler."""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import Mock

import pytest

from f_lib.logging._console_handler import ConsoleHandler

if TYPE_CHECKING:
    from pytest_mock import MockerFixture

MODULE = "f_lib.logging._console_handler"


class TestConsoleHandler:
    """Test ConsoleHandler."""

    @pytest.mark.parametrize(
        ("escape", "markup", "expected"),
        [(False, False, False), (False, True, False), (True, False, False), (True, True, True)],
    )
    def test__determine_should_escape(
        self, escape: bool, expected: bool, markup: bool, mocker: MockerFixture
    ) -> None:
        """Test _determine_should_escape."""
        determine_use_markup = mocker.patch.object(
            ConsoleHandler, "_determine_use_markup", return_value=markup
        )
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
    def test__determine_use_markup(
        self, expected: bool, handler_markup: bool, record_markup: bool | None
    ) -> None:
        """Test _determine_use_markup."""
        record = Mock(markup=record_markup)
        if record_markup is None:
            del record.markup
        assert ConsoleHandler(markup=handler_markup)._determine_use_markup(record) is expected

    def test__style_message(self, mocker: MockerFixture) -> None:
        """Test _style_message."""
        record = Mock()
        determine_use_markup = mocker.patch.object(
            ConsoleHandler, "_determine_use_markup", return_value=False
        )
        from_markup = mocker.patch(f"{MODULE}.Text.from_markup")
        assert ConsoleHandler()._style_message(record, "msg") == (record, "msg")
        determine_use_markup.assert_called_once_with(record)
        from_markup.assert_not_called()

    def test__style_message_markup(self, mocker: MockerFixture) -> None:
        """Test _style_message with markup."""
        record = Mock(levelname="INFO")
        determine_use_markup = mocker.patch.object(
            ConsoleHandler, "_determine_use_markup", return_value=True
        )
        from_markup = mocker.patch(
            f"{MODULE}.Text.from_markup", return_value=Mock(markup="success")
        )
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
        determine_should_escape = mocker.patch.object(
            ConsoleHandler, "_determine_should_escape", return_value=True
        )
        escape = mocker.patch(f"{MODULE}.escape", return_value="escaped")
        render_message = mocker.patch(
            f"{MODULE}.RichHandler.render_message", return_value="rendered"
        )
        style_message = mocker.patch.object(
            ConsoleHandler, "_style_message", return_value=("style", "message")
        )
        assert ConsoleHandler().render_message(record, "message") == render_message.return_value
        determine_should_escape.assert_called_once_with(record)
        escape.assert_called_once_with("message")
        style_message.assert_called_once_with(record, "escaped")
        render_message.assert_called_once_with("style", "message")
