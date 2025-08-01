"""Test f_lib.archive_extractor._tar_extractor."""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import MagicMock, Mock

import pytest

from f_lib.archive_extractor._tar_extractor import TarExtractor
from f_lib.archive_extractor.exceptions import ArchiveTypeError, Pep706Error

from ...utils import get_archive_fixture

if TYPE_CHECKING:
    from pathlib import Path

    from pytest_mock import MockerFixture

    from ...utils import ArchiveFixtureLiteral

MODULE = "f_lib.archive_extractor._tar_extractor"


class TestTarExtractor:
    """Test TarExtractor."""

    def test___init___raise_archive_type_error(self, zip_file: Path) -> None:
        """Test __init__ raises ArchiveTypeError."""
        with pytest.raises(ArchiveTypeError, match="suffix supported by this extractor"):
            TarExtractor(zip_file)

    @pytest.mark.parametrize("archive_name", ["bz2_file", "gz_file", "gzip_file", "tar_file", "xz_file"])
    def test_extract(
        self,
        archive_name: ArchiveFixtureLiteral,
        mocker: MockerFixture,
        request: pytest.FixtureRequest,
        tmp_path: Path,
    ) -> None:
        """Test extract."""
        mocker.patch(f"{MODULE}.tarfile.data_filter")
        archive = get_archive_fixture(request, archive_name)
        extract = Mock()
        tarfile_open = mocker.patch(
            f"{MODULE}.tarfile.open",
            return_value=MagicMock(__enter__=Mock(return_value=Mock(extractall=extract))),
        )
        assert TarExtractor(archive).extract(tmp_path) == tmp_path
        tarfile_open.assert_called_once_with(archive, mode="r:*")
        extract.assert_called_once_with(tmp_path, filter="data")

    def test_extract_raise_pep706(self, mocker: MockerFixture, tmp_path: Path) -> None:
        """Test extract raises Pep706Error."""
        tar_file = mocker.patch(f"{MODULE}.tarfile")
        del tar_file.data_filter
        tmp_file = tmp_path / "file.tar"
        tmp_file.touch()
        with pytest.raises(Pep706Error):
            TarExtractor(tmp_file).extract(tmp_path)
