"""Environment object class."""

import json
import logging
import os
from pathlib import Path
from typing import Self

from ._system_info import SystemInfo

LOGGER = logging.getLogger(__name__)


class Environment:
    """Object to simplify getting information about the runtime environment."""

    root_dir: Path
    """Root directory of the environment."""

    sys: SystemInfo
    """Information about the system."""

    def __init__(
        self,
        *,
        environ: dict[str, str] | None = None,
        root_dir: Path | None = None,
    ) -> None:
        """Instantiate class.

        Args:
            environ: Environment variables.
            root_dir: Root directory of the environment (e.g. :meth:`pathlib.Path.cwd`).

        """
        self.root_dir = root_dir or Path.cwd()
        self.sys = SystemInfo()
        self.vars = environ if isinstance(environ, dict) else os.environ.copy()

    @property
    def ci(self) -> bool:
        """Return CI status.

        Returns:
            bool

        """
        return "CI" in self.vars

    @ci.setter
    def ci(self, value: object) -> None:
        """Set the value of CI."""
        if value:
            self._update_vars({"CI": "1"})
        else:
            self.vars.pop("CI", None)

    @ci.deleter
    def ci(self) -> None:
        """Delete the value of CI."""
        self.vars.pop("CI", None)

    @property
    def debug(self) -> bool:
        """Get debug setting from the environment."""
        return "DEBUG" in self.vars

    @debug.setter
    def debug(self, value: object) -> None:
        """Set the value of DEBUG."""
        if value:
            self._update_vars({"DEBUG": "1"})
        else:
            self.vars.pop("DEBUG", None)

    @property
    def verbose(self) -> bool:
        """Get verbose setting from the environment."""
        return "VERBOSE" in self.vars

    @verbose.setter
    def verbose(self, value: object) -> None:
        """Set the value of VERBOSE."""
        if value:
            self._update_vars({"VERBOSE": "1"})
        else:
            self.vars.pop("VERBOSE", None)

    def copy(self: Self) -> Self:
        """Copy the contents of this object into a new instance.

        Returns:
            New instance with the same contents.

        """
        return self.__class__(
            environ=self.vars.copy(),
            root_dir=self.root_dir,
        )

    def _update_vars(self, env_vars: dict[str, str]) -> None:
        """Update vars and log the change.

        Args:
            env_vars (Dict[str, str]): Dict to update self.vars with.

        """
        self.vars.update(env_vars)
        LOGGER.debug("updated environment variables: %s", json.dumps(env_vars))

    def __bool__(self) -> bool:
        """Evaluation of instances as a bool."""
        return bool(self.vars)

    def __eq__(self, other: object) -> bool:
        """Compare self with another object for equality."""
        if isinstance(other, self.__class__):
            return bool(self.root_dir == other.root_dir and self.vars == other.vars)
        return NotImplemented

    def __ne__(self, other: object) -> bool:
        """Compare self with another object for inequality."""
        return not self == other
