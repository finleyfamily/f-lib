"""Test f_lib.archive_extractor._zip_extractor."""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import MagicMock, Mock

import pytest

from f_lib.archive_extractor._zip_extractor import ZipExtractor
from f_lib.archive_extractor.exceptions import ArchiveTypeError

if TYPE_CHECKING:
    from pathlib import Path

    from pytest_mock import MockerFixture

MODULE = "f_lib.archive_extractor._zip_extractor"


class TestZipExtractor:
    """Test ZipExtractor."""

    def test___init___raise_archive_type_error(self, tar_file: Path) -> None:
        """Test __init__ raises ArchiveTypeError."""
        with pytest.raises(ArchiveTypeError, match="suffix supported by this extractor"):
            ZipExtractor(tar_file)

    def test_extract(self, mocker: MockerFixture, tmp_path: Path, zip_file: Path) -> None:
        """Test extract."""
        extract = Mock()
        zipfile_kls = mocker.patch(
            f"{MODULE}.ZipFile",
            return_value=MagicMock(__enter__=Mock(return_value=Mock(extractall=extract))),
        )
        assert ZipExtractor(zip_file).extract(tmp_path) == tmp_path
        zipfile_kls.assert_called_once_with(zip_file, mode="r")
        extract.assert_called_once_with(tmp_path)
