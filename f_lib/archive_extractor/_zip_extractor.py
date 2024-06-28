"""Extractor for ``.zip`` archives."""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar
from zipfile import ZipFile

from ._archive_extractor import ArchiveExtractor

if TYPE_CHECKING:
    from pathlib import Path


class ZipExtractor(ArchiveExtractor):
    """Extractor for ``.zip`` archives."""

    SUFFIX: ClassVar[tuple[str, ...]] = (".zip",)
    """File extension/suffix supported by the extractor."""

    def extract(self, destination: Path) -> Path:
        """Extract the archive file.

        Args:
            destination: Where the archive file will be extracted to.

        Returns:
            Path to the extraction.

        """
        destination.mkdir(exist_ok=True, parents=True)
        with ZipFile(self.archive, mode="r") as file_obj:
            file_obj.extractall(destination)
        return destination
