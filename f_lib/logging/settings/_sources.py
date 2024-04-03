"""Custom config sources."""

from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, TomlConfigSettingsSource


class PyprojectTomlConfigSettingsSource(TomlConfigSettingsSource):
    """pyproject.toml config settings source."""

    def __init__(
        self,
        settings_cls: type[BaseSettings],
        toml_file: Path | None = None,
    ) -> None:  # cov: ignore
        """Instantiate class."""
        self.table_path: tuple[str, ...] = settings_cls.model_config.get("toml_table_path", ())
        self.toml_file_path = self._pick_pyproject_toml_file(toml_file)
        self.toml_data = self._read_files(self.toml_file_path)
        for key in self.table_path:
            self.toml_data = self.toml_data.get(key, {})
        super(TomlConfigSettingsSource, self).__init__(settings_cls, self.toml_data)

    @staticmethod
    def _pick_pyproject_toml_file(provided: Path | None) -> Path:  # cov: ignore
        """Pick a pyproject.toml file path to use."""
        if provided:
            return provided.resolve()
        rv = Path.cwd() / "pyproject.toml"
        if not rv.is_file():
            other = rv.parent.parent / "pyproject.toml"
            if other.is_file():
                return other
        return rv
