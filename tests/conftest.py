"""Pytest configuration, fixtures, and plugins."""
from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Iterator


@pytest.fixture()
def cd_tmp_path(tmp_path: Path) -> Iterator[Path]:
    """Change directory to a temporary path.

    Returns:
        Path: Temporary path object.

    """
    prev_dir = Path.cwd()
    os.chdir(tmp_path)
    try:
        yield tmp_path
    finally:
        os.chdir(prev_dir)
