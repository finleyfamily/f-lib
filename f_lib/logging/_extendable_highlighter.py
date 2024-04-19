"""Custom :class:`~rich.highlighter.Highlighter`."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, ClassVar, TypedDict

from rich.highlighter import Highlighter, ReprHighlighter

if TYPE_CHECKING:
    from rich.text import Text


class HighlightTypedDict(TypedDict):
    """:class:`typing.TypedDict` for highlights.

    Used with :class:`f_lib.logging.ExtendableHighlighter`.

    """

    base_style: str
    """Base name used for applying styles."""

    highlights: list[str] | tuple[str, ...]
    """Regex patterns to highlight."""


class ExtendableHighlighter(Highlighter):
    """Extendable :class:`~rich.highlighter.Highlighter`."""

    __slots__ = ()

    DEFAULT_HIGHLIGHTS: ClassVar[tuple[HighlightTypedDict, ...]] = (
        HighlightTypedDict(
            base_style=ReprHighlighter.base_style, highlights=ReprHighlighter.highlights
        ),
        HighlightTypedDict(
            base_style="aws.",
            highlights=(
                r"(?P<region>(us(-gov)?|ap|ca|cn|eu|sa)-(central|(north|south)?(east|west)?)-\d)",
            ),
        ),
        HighlightTypedDict(
            base_style="aws.cloudformation.",
            highlights=(
                r"(?P<capabilities>(CAPABILITY_IAM|CAPABILITY_NAMED_IAM|CAPABILITY_AUTO_EXPAND))",
                r"(?P<status>(CREATE_COMPLETE|CREATE_FAILED|CREATE_IN_PROGRESS|DELETE_COMPLETE|"
                "DELETE_FAILED|DELETE_IN_PROGRESS|IMPORT_COMPLETE|IMPORT_IN_PROGRESS|"
                "IMPORT_ROLLBACK_COMPLETE|IMPORT_ROLLBACK_FAILED|IMPORT_ROLLBACK_IN_PROGRESS|"
                "REVIEW_IN_PROGRESS|ROLLBACK_COMPLETE|ROLLBACK_FAILED|ROLLBACK_IN_PROGRESS|"
                "UPDATE_COMPLETE|UPDATE_COMPLETE_CLEANUP_IN_PROGRESS|UPDATE_FAILED|"
                "UPDATE_IN_PROGRESS|UPDATE_ROLLBACK_COMPLETE|"
                "UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS|UPDATE_ROLLBACK_FAILED|"
                "UPDATE_ROLLBACK_IN_PROGRESS))",
                r"(?P<detailed_status>(CONFIGURATION_COMPLETE|VALIDATION_FAILED))",
            ),
        ),
    )

    HIGHLIGHTS: ClassVar[tuple[HighlightTypedDict, ...]] = ()

    @cached_property
    def highlights(self) -> tuple[HighlightTypedDict, ...]:
        """All highlights of this highlighter."""
        return self.DEFAULT_HIGHLIGHTS + self.HIGHLIGHTS

    def highlight(self, text: Text) -> None:
        """Highlight :class:`rich.text.Text` using regular expressions.

        Args:
            text: Text to highlighted.

        """
        for highlight in self.highlights:
            for pattern in highlight["highlights"]:
                text.highlight_regex(pattern, style_prefix=highlight["base_style"])
