"""Operating system information."""

from __future__ import annotations

import os
import platform
from functools import cached_property
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar, cast, final

from platformdirs.unix import Unix
from platformdirs.windows import Windows

if TYPE_CHECKING:
    import platformdirs


@final
class OsInfo:
    """Information about the operating system running on the current system."""

    __instance: ClassVar[OsInfo | None] = None

    def __new__(cls, *args: object, **kwargs: object) -> OsInfo:
        """Create a new instance of class.

        This class is a singleton so it will always return the same instance.

        """
        if cls.__instance is None:
            cls.__instance = cast(OsInfo, super().__new__(cls, *args, **kwargs))
        return cls.__instance

    @cached_property
    def _platform_dirs(self) -> platformdirs.PlatformDirsABC:
        """Instance of platformdirs class to get platform specific directories.

        ``appname``, ``appauthor``, and ``version`` are not passed to the class.
        This is so that the base directory is returned.

        """
        if self.is_windows:
            return Windows(appname="f-lib", appauthor="finley")
        # platformdirs does no handle macOS the way I would like it to so alway use unix
        return Unix(appname="f-lib", appauthor="finley")

    @cached_property
    def is_darwin(self) -> bool:
        """Operating system is Darwin."""
        return self.name == "darwin"

    @cached_property
    def is_linux(self) -> bool:
        """Operating system is Linux."""
        return self.name == "linux"

    @cached_property
    def is_macos(self) -> bool:
        """Operating system is macOS.

        Does not differentiate between macOS and Darwin.

        """
        return self.is_darwin

    @cached_property
    def is_posix(self) -> bool:
        """Operating system is posix."""
        return os.name == "posix"

    @cached_property
    def is_windows(self) -> bool:
        """Operating system is Windows."""
        return self.name in ("windows", "mingw64", "msys_nt", "cygwin_nt")

    @cached_property
    def name(self) -> str:
        """Operating system name set to lowercase for consistency."""
        return platform.system().lower()

    @cached_property
    def user_config_dir(self) -> Path:
        """Path to the config directory for the user.

        - ``~/.config``
        - ``%USERPROFILE%/AppData/Local``
        - ``%USERPROFILE%/AppData/Roaming``

        """
        return Path(self._platform_dirs.user_config_dir)

    @cached_property
    def user_data_dir(self) -> Path:
        """Path to data directory tied to the user.

        - ``~/.local/share``
        - ``%USERPROFILE%/AppData/Local``
        - ``%USERPROFILE%/AppData/Roaming``

        """
        return Path(self._platform_dirs.user_data_dir)

    @classmethod
    def clear_singleton(cls) -> None:
        """Clear singleton instances.

        Intended to only be used for running tests.

        """
        cls.__instance = None

    def __bool__(self) -> bool:
        """Evaluation of instances as a bool."""
        return True

    def __eq__(self, other: object) -> bool:
        """Compare self with another object for equality."""
        return id(self) == id(other)

    def __ne__(self, other: object) -> bool:
        """Compare self with another object for inequality."""
        return not self == other
