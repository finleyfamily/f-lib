"""Pytest configuration, fixtures, and plugins."""

from __future__ import annotations

import shutil
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture()
def bz2_file(fixture_dir: Path, tmp_path: Path) -> Path:
    """Path to the ``.tar.bz2`` fixture, copying it into the ``tmp_path``."""
    return shutil.copyfile(fixture_dir / "src.tar.bz2", tmp_path / "src.tar.bz2")


@pytest.fixture()
def gz_file(fixture_dir: Path, tmp_path: Path) -> Path:
    """Path to the ``.tar.gz`` fixture, copying it into the ``tmp_path``."""
    return shutil.copyfile(fixture_dir / "src.tar.gz", tmp_path / "src.tar.gz")


@pytest.fixture()
def gzip_file(fixture_dir: Path, tmp_path: Path) -> Path:
    """Path to the ``.gzip`` fixture, copying it into the ``tmp_path``."""
    return shutil.copyfile(fixture_dir / "src.gzip", tmp_path / "src.gzip")


@pytest.fixture()
def tar_file(fixture_dir: Path, tmp_path: Path) -> Path:
    """Path to the ``.tar`` fixture, copying it into the ``tmp_path``."""
    return shutil.copyfile(fixture_dir / "src.tar", tmp_path / "src.tar")


@pytest.fixture()
def xz_file(fixture_dir: Path, tmp_path: Path) -> Path:
    """Path to the ``.tar.xz`` fixture, copying it into the ``tmp_path``."""
    return shutil.copyfile(fixture_dir / "src.tar.xz", tmp_path / "src.tar.xz")


@pytest.fixture()
def zip_file(fixture_dir: Path, tmp_path: Path) -> Path:
    """Path to the ``.zip`` fixture, copying it into the ``tmp_path``."""
    return shutil.copyfile(fixture_dir / "src.zip", tmp_path / "src.zip")
