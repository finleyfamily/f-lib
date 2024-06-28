"""Abstract base class for archive extractors."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import ClassVar, Literal

from .exceptions import ArchiveTypeError


class ArchiveExtractor(ABC):
    """Abstract base class for archive extractors."""

    SUFFIX: ClassVar[tuple[str, ...]] = ()
    """File extension/suffix supported by the extractor."""

    archive: Path
    """Resolved path to the archive file."""

    def __init__(self, archive: Path | str, *, strict: bool = True) -> None:
        """Instantiate class.

        Args:
            archive: Path to the archive file.
            strict: Raise an error if the provided archive file does not have the
                expected file extension/suffix.

        """
        self.archive = Path(archive).resolve()

        if not self.archive.is_file():
            raise FileNotFoundError(self.archive)

        if strict and self.SUFFIX and not self.can_extract(self.archive):
            raise ArchiveTypeError(self.archive, self.SUFFIX)

    @abstractmethod
    def extract(self, destination: Path) -> Path:
        """Extract the archive file.

        Args:
            destination: Where the archive file will be extracted to.

        Returns:
            Path to the extraction.

        """

    @classmethod
    def can_extract(cls, archive: Path | str) -> bool:
        """Determine if the extractor can attempt to extract the file.

        Args:
            archive: Path to an archive file.

        """
        path = Path(archive)  # ensure it's a path object
        if not path.is_file():
            return False
        return any(True for suffix in cls.SUFFIX if "".join(path.suffixes).endswith(suffix))

    def __bool__(self) -> Literal[True]:
        return True

    def __str__(self) -> str:
        return str(self.archive)
