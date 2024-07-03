"""System information."""

from __future__ import annotations

import platform
import sys
from functools import cached_property
from typing import ClassVar, Literal, cast, final

from ._os_info import OsInfo


class UnknownPlatformArchitectureError(Exception):
    """Raised when the platform architecture can't be determined."""

    def __init__(self, value: str) -> None:
        """Instantiate class.

        Args:
            value: The value causing the architecture to be unknown.

        """
        super().__init__(f"Unknown system architecture detected! ({value})")


@final
class SystemInfo:
    """Information about the system running the application."""

    __instance: ClassVar[SystemInfo | None] = None

    def __new__(cls, *args: object, **kwargs: object) -> SystemInfo:
        """Create a new instance of class.

        This class is a singleton so it will always return the same instance.

        """
        if cls.__instance is None:
            cls.__instance = cast(SystemInfo, super().__new__(cls, *args, **kwargs))
        return cls.__instance

    @cached_property
    def architecture(self) -> Literal["amd32", "amd64", "arm32", "arm64"]:
        """System's CPU architecture."""
        if self.is_arm:
            if self.is_64bit:
                return "arm64"
            return "arm32"
        if self.is_x86:
            if self.is_64bit:
                return "amd64"
            return "amd32"
        raise UnknownPlatformArchitectureError(platform.machine())

    @cached_property
    def is_32bit(self) -> bool:
        """Whether the system is 32-bit."""
        return sys.maxsize <= 2**32

    @cached_property
    def is_64bit(self) -> bool:
        """Whether the system is 64-bit."""
        return sys.maxsize > 2**32

    @cached_property
    def is_arm(self) -> bool:
        """Whether the system is arm based."""
        return platform.machine().lower().startswith(("arm", "aarch"))

    @cached_property
    def is_frozen(self) -> bool:
        """Whether or not app is running from a frozen package."""
        return bool(getattr(sys, "frozen", False))

    @cached_property
    def is_x86(self) -> bool:
        """Whether the system is x86."""
        return platform.machine().lower() in ("i386", "amd64", "x86_64")

    @cached_property
    def os(self) -> OsInfo:
        """Operating system information."""
        return OsInfo()

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
