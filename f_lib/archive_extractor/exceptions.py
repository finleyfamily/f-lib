"""Archive extractor exceptions."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Sequence
    from pathlib import Path


class ArchiveTypeError(Exception):
    """Raised when the supplied archive is not of a supported type."""

    archive: Path
    supported_suffix: Sequence[str]

    def __init__(self, archive: Path, supported_suffix: Sequence[str]) -> None:
        """Instantiate class."""
        self.archive = archive
        self.supported_suffix = supported_suffix
        archive_suffix = "".join(archive.suffixes)
        joined_suffix = ", ".join(supported_suffix)
        super().__init__(
            f"archive {archive.name} ({archive_suffix}) doesn't have "
            f"a suffix supported by this extractor ({joined_suffix})"
        )

    def __reduce__(self) -> tuple[type[Exception], tuple[Any, ...]]:
        """Exception pickling support.

        https://github.com/python/cpython/issues/44791

        """
        return self.__class__, (self.archive, self.supported_suffix)


class Pep706Error(Exception):
    """Raised when the current version of Python contains a security vulnerability."""

    def __init__(self) -> None:
        """Instantiate class."""
        super().__init__(
            "Current version of Python contains the security vulnerability discussed in PEP 706. "
            "Update to a version of Python containing the discussed security update."
        )
