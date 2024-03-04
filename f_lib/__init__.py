"""Finley library."""

import logging as __logging
from importlib.metadata import PackageNotFoundError, version

from . import aws, constants, logging, mixins, utils
from ._environment import Environment
from ._os_info import OsInfo
from ._system_info import SystemInfo, UnknownPlatformArchitectureError

# when creating loggers, always use instances of `f_lib.logging.Logger`
__logging.setLoggerClass(logging.Logger)

try:
    __version__ = version(__name__)
except PackageNotFoundError:  # cov: ignore
    # package is not installed
    __version__ = "0.0.0"


__all__ = [
    "Environment",
    "OsInfo",
    "SystemInfo",
    "aws",
    "constants",
    "logging",
    "mixins",
    "utils",
    "UnknownPlatformArchitectureError",
]
