"""Finley library."""

import logging as __logging

from . import aws, constants, logging, mixins, utils
from ._environment import Environment
from ._os_info import OsInfo
from ._system_info import SystemInfo, UnknownPlatformArchitectureError

# when creating loggers, always use instances of `f_lib.logging.Logger`
__logging.setLoggerClass(logging.Logger)

__version__: str = "0.0.0"
"""Version of the Python package presented as a :class:`string`.

Dynamically set upon release by [poetry-dynamic-versioning](https://github.com/mtkennerly/poetry-dynamic-versioning).

"""

__version_tuple__: tuple[int, int, int] | tuple[int, int, int, str] = (0, 0, 0)
"""Version of the Python package presented as a :class:`tuple`.

Dynamically set upon release by [poetry-dynamic-versioning](https://github.com/mtkennerly/poetry-dynamic-versioning).

"""


__all__ = [
    "Environment",
    "OsInfo",
    "SystemInfo",
    "UnknownPlatformArchitectureError",
    "aws",
    "constants",
    "logging",
    "mixins",
    "utils",
]
