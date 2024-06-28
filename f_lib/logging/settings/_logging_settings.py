"""Logging configuration model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic_settings import BaseSettings, PyprojectTomlConfigSettingsSource
from pydantic_settings import SettingsConfigDict as BaseSettingsConfigDict

from ._console_logging_settings import ConsoleLoggingSettings

if TYPE_CHECKING:
    from pydantic_settings import PydanticBaseSettingsSource


class _SettingsConfigDict(BaseSettingsConfigDict, total=False):
    """Overrides SettingsConfigDict to add pyproject.toml settings."""

    toml_table_path: tuple[str, ...]
    """Path to the table to load.

    .. rubric:: Example
    .. code-block:: toml
        :caption: pyproject.toml

        [tool.poetry]

    .. code-block:: python

        SettingsConfigDict(toml_table_path=("tool", "poetry"))

    """


class LoggingSettings(BaseSettings):
    """Top-level logging settings."""

    model_config = _SettingsConfigDict(
        env_ignore_empty=True,
        env_nested_delimiter="__",
        env_prefix="F_LOGGING_",
        pyproject_toml_table_header=("tool", "f", "logging"),
    )

    console: ConsoleLoggingSettings = ConsoleLoggingSettings()
    """Settings for console logging."""

    @classmethod
    def settings_customise_sources(  # cspell:ignore customise
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Enable ``pyproject.toml`` source."""
        return (
            PyprojectTomlConfigSettingsSource(settings_cls),
            dotenv_settings,
            env_settings,
            file_secret_settings,
            init_settings,
        )

    def __bool__(self) -> bool:
        return True
