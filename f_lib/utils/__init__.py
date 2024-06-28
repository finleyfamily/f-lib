"""Utilities."""

from __future__ import annotations

import platform
import shlex
import subprocess
from typing import TYPE_CHECKING, Any, cast

from ._file_hash import FileHash

if TYPE_CHECKING:
    import pathlib
    from collections.abc import Iterable


def convert_kwargs_to_shell_list(
    **kwargs: bool | Iterable[pathlib.Path] | Iterable[str] | str | None,
) -> list[str]:
    """Convert kwargs to a list of shell arguments."""
    result: list[str] = []
    for k, v in kwargs.items():
        if isinstance(v, str):
            result.extend([convert_to_cli_flag(k), v])
        elif isinstance(v, list | set | tuple):
            for i in cast("Iterable[Any]", v):
                result.extend([convert_to_cli_flag(k), str(i)])
        elif isinstance(v, bool) and v:
            result.append(convert_to_cli_flag(k))
    return result


def convert_list_to_shell_str(split_command: Iterable[str]) -> str:
    """Combine a list of strings into a string that can be run as a command.

    Handles multi-platform differences.

    """
    if platform.system() == "Windows":
        return subprocess.list2cmdline(split_command)
    return shlex.join(split_command)


def convert_to_cli_flag(arg_name: str, *, prefix: str = "--") -> str:
    """Convert string kwarg name into a CLI flag."""
    return f"{prefix}{arg_name.replace('_', '-')}"


__all__ = [
    "FileHash",
    "convert_kwargs_to_shell_list",
    "convert_list_to_shell_str",
    "convert_to_cli_flag",
]
