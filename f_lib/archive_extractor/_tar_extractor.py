"""Extractor for ``.tar`` archives."""

from __future__ import annotations

import tarfile
from typing import TYPE_CHECKING, ClassVar

from ._archive_extractor import ArchiveExtractor
from .exceptions import Pep706Error

if TYPE_CHECKING:
    from pathlib import Path


class TarExtractor(ArchiveExtractor):
    """Extractor for ``.tar`` archives.

    Supports bz2, gz, and xz compression types.

    """

    SUFFIX: ClassVar[tuple[str, ...]] = (
        ".gzip",
        ".tar",
        ".tar.gz",
        ".tar.bz2",
        ".tar.xz",
    )
    """File extension/suffix supported by the extractor."""

    def extract(self, destination: Path) -> Path:
        """Extract the archive file.

        Args:
            destination: Where the archive file will be extracted to.

        Returns:
            Path to the extraction.

        """
        if not hasattr(tarfile, "data_filter"):
            raise Pep706Error
        destination.mkdir(exist_ok=True, parents=True)
        with tarfile.open(self.archive, mode="r:*") as file_obj:
            file_obj.extractall(destination.resolve(), filter="data")
        return destination
