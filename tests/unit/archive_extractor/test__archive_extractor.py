"""Test f_lib.archive_extractor._archive_extractor."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from f_lib.archive_extractor._archive_extractor import ArchiveExtractor
from f_lib.archive_extractor.exceptions import ArchiveTypeError

if TYPE_CHECKING:
    from pathlib import Path

    from pytest_mock import MockerFixture


class Extractor(ArchiveExtractor):
    """Subclass as Extractor is an ABC."""

    def extract(self, destination: Path) -> Path:  # noqa: D102
        return destination


class TestArchiveExtractor:
    """Test ArchiveExtractor."""

    def test___init__(self, gz_file: Path) -> None:
        """Test __init__."""
        obj = Extractor(str(gz_file))
        assert obj.archive == gz_file

    def test___init___can_extract(self, gz_file: Path, mocker: MockerFixture) -> None:
        """Test __init__."""
        can_extract = mocker.patch.object(Extractor, "can_extract", return_value=True)
        mocker.patch.object(Extractor, "SUFFIX", (".gz",))
        assert Extractor(gz_file)  # suffix is ".tar.gz"
        can_extract.assert_called_once_with(gz_file)

    def test___init___not_strict(self, gz_file: Path, mocker: MockerFixture) -> None:
        """Test __init__."""
        can_extract = mocker.patch.object(Extractor, "can_extract", return_value=False)
        mocker.patch.object(Extractor, "SUFFIX", (".zip",))
        assert Extractor(gz_file, strict=False)
        can_extract.assert_not_called()

    def test___init___raise_file_not_found(self, mocker: MockerFixture, tmp_path: Path) -> None:
        """Test __init__ raises FileNotFoundError."""
        can_extract = mocker.patch.object(Extractor, "can_extract", return_value=True)
        with pytest.raises(FileNotFoundError):
            Extractor(tmp_path / "foo")
        can_extract.assert_not_called()

    def test___init___raise_value_error(self, gz_file: Path, mocker: MockerFixture) -> None:
        """Test __init__ raises ValueError."""
        can_extract = mocker.patch.object(Extractor, "can_extract", return_value=False)
        mocker.patch.object(Extractor, "SUFFIX", (".txt",))
        with pytest.raises(ArchiveTypeError, match="suffix supported by this extractor"):
            Extractor(gz_file)
        can_extract.assert_called_once_with(gz_file)

    def test___str__(self, gz_file: Path) -> None:
        """Test __str__."""
        assert str(Extractor(gz_file)) == str(gz_file)

    def test_can_extract(self, gz_file: Path, mocker: MockerFixture) -> None:
        """Test can_extract."""
        mocker.patch.object(Extractor, "SUFFIX", (".gz",))
        assert Extractor.can_extract(gz_file)

    def test_can_extract_false(self, gz_file: Path, mocker: MockerFixture) -> None:
        """Test can_extract False."""
        mocker.patch.object(Extractor, "SUFFIX", (".txt",))
        assert not Extractor.can_extract(gz_file)

    def test_can_extract_false_file_not_found(self, tmp_path: Path) -> None:
        """Test can_extract False due to file not found."""
        assert not Extractor.can_extract(tmp_path)
