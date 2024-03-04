"""Test f_lib.logging._highlighters."""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import Mock, call

from f_lib.logging._highlighters import ExtendableHighlighter

if TYPE_CHECKING:
    from pytest_mock import MockerFixture


class TestExtendableHighlighter:
    """Test ExtendableHighlighter."""

    def test_highlight(self, mocker: MockerFixture) -> None:
        """Test highlight."""
        highlight_regex = Mock()
        mocker.patch.object(
            ExtendableHighlighter,
            "highlights",
            new=(
                {"base_style": "foo.", "highlights": ("foo.highlight0", "foo.highlight1")},
                {"base_style": "bar.", "highlights": ("bar.highlight",)},
            ),
        )
        assert not ExtendableHighlighter().highlight(Mock(highlight_regex=highlight_regex))
        highlight_regex.assert_has_calls(
            (
                call("foo.highlight0", style_prefix="foo."),
                call("foo.highlight1", style_prefix="foo."),
                call("bar.highlight", style_prefix="bar."),
            )
        )

    def test_highlights(self, mocker: MockerFixture) -> None:
        """Test highlights."""
        mocker.patch.object(ExtendableHighlighter, "DEFAULT_HIGHLIGHTS", ("foo",))
        mocker.patch.object(ExtendableHighlighter, "HIGHLIGHTS", ("bar",))
        assert ExtendableHighlighter().highlights == ("foo", "bar")
