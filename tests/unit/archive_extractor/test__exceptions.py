"""Test f_lib.archive_extractor.exceptions."""

from __future__ import annotations

import pickle
from typing import TYPE_CHECKING

from f_lib.archive_extractor.exceptions import ArchiveTypeError

if TYPE_CHECKING:
    from pathlib import Path


class TestArchiveTypeError:
    """Test ArchiveTypeError."""

    def test_pickle(self, tmp_path: Path) -> None:
        """Test pickling."""
        archive = tmp_path / "foo.zip"
        suffix = (".tar", ".tar.gz")
        exc = ArchiveTypeError(archive, suffix)

        round_trip = pickle.loads(pickle.dumps(exc))
        assert str(round_trip) == str(exc)
        assert round_trip.archive == exc.archive
        assert round_trip.supported_suffix == exc.supported_suffix
