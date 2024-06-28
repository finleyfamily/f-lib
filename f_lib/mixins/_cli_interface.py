"""CLI interface mixin."""

from __future__ import annotations

import logging
import shutil
import subprocess
from typing import IO, TYPE_CHECKING, ClassVar, Literal, cast, overload

from ..constants import ANSI_ESCAPE_PATTERN
from ..utils import convert_kwargs_to_shell_list, convert_list_to_shell_str

if TYPE_CHECKING:
    import pathlib
    from collections.abc import Iterable

    from .._environment import Environment

LOGGER = logging.getLogger(__name__)


class CliInterfaceMixin:
    """Mixin for adding CLI interface methods."""

    EXECUTABLE: ClassVar[str]
    """CLI executable."""

    env: Environment
    """Environment."""

    cwd: pathlib.Path
    """Working directory where commands will be run."""

    @classmethod
    def found_in_path(cls) -> bool:
        """Determine if executable is found in $PATH."""
        return bool(shutil.which(cls.EXECUTABLE))

    @classmethod
    def generate_command(
        cls,
        __command: list[str] | str | None = None,
        **kwargs: bool | Iterable[pathlib.Path] | Iterable[str] | str | None,
    ) -> list[str]:
        """Generate command to be executed and log it.

        Args:
            __command: Command to run.
            **kwargs: Additional args to pass to the command.

        Returns:
            The full command to be passed into a subprocess.

        """
        cmd = [
            cls.EXECUTABLE,
            *(__command if isinstance(__command, list) else ([__command] if __command else [])),
        ]
        cmd.extend(convert_kwargs_to_shell_list(**kwargs))
        LOGGER.debug("generated command: %s", convert_list_to_shell_str(cmd))
        return cmd

    @overload
    def _run_command(
        self,
        command: Iterable[str] | str,
        *,
        capture_output: Literal[True],
        env: dict[str, str] | None = ...,
        timeout: float | None = ...,
    ) -> str: ...

    @overload
    def _run_command(
        self,
        command: Iterable[str] | str,
        *,
        capture_output: Literal[True],
        env: dict[str, str] | None = ...,
        suppress_output: Literal[False],
        timeout: float | None = ...,
    ) -> str: ...

    @overload
    def _run_command(
        self,
        command: Iterable[str] | str,
        *,
        capture_output: bool = ...,
        env: dict[str, str] | None = ...,
        suppress_output: Literal[True] = ...,
        timeout: float | None = ...,
    ) -> str: ...

    @overload
    def _run_command(
        self,
        command: Iterable[str] | str,
        *,
        env: dict[str, str] | None = ...,
        suppress_output: Literal[False],
        timeout: float | None = ...,
    ) -> None: ...

    @overload
    def _run_command(
        self,
        command: Iterable[str] | str,
        *,
        capture_output: bool = ...,
        env: dict[str, str] | None = ...,
        suppress_output: bool = ...,
        timeout: float | None = ...,
    ) -> str | None: ...

    def _run_command(
        self,
        command: Iterable[str] | str,
        *,
        capture_output: bool = False,
        env: dict[str, str] | None = None,
        suppress_output: bool = True,
        timeout: float | None = None,
    ) -> str | None:
        """Run command.

        Args:
            command: Command to pass to shell to execute.
            capture_output: Whether to capture output.
                This can be used when not wanting to suppress output but still needing
                to process the contents. The output will be buffered and returned as a
                string. If ``suppress_output`` is ``True``, this will be ignored.
            env: Environment variables.
            suppress_output: If ``True``, the output of the subprocess written
                to ``sys.stdout`` and ``sys.stderr`` will be captured and
                returned as a string instead of being being written directly.
            timeout: Number of seconds to wait before terminating the child process.
                Internally passed on to :meth:`~subprocess.Popen.communicate`.

        """
        cmd_str = command if isinstance(command, str) else convert_list_to_shell_str(command)
        LOGGER.debug("running command: %s", cmd_str)
        if suppress_output:
            return subprocess.check_output(  # noqa: S602
                cmd_str,
                cwd=self.cwd,
                env=env or self.env.vars,
                shell=True,
                stderr=subprocess.STDOUT,  # forward stderr to stdout so it is captured
                text=True,
                timeout=timeout,
            )
        if capture_output:
            return self._run_command_capture_output(cmd_str, env=env or self.env.vars)
        subprocess.check_call(  # noqa: S602
            cmd_str,
            cwd=self.cwd,
            env=env or self.env.vars,
            shell=True,
            timeout=timeout,
        )
        return None

    def _run_command_capture_output(
        self,
        command: str,
        *,
        env: dict[str, str] | None = None,
        timeout: float | None = None,
    ) -> str:
        """Run command and capture output while still allowing it to be printed.

        Intended to be called from ``_run_command``.

        Args:
            command: Command to pass to shell to execute.
            env: Environment variables.
            timeout: Number of seconds to wait before terminating the child process.

        """
        output_list: list[str] = []  # accumulate output from the buffer
        with subprocess.Popen(  # noqa: S602
            command,
            bufsize=1,
            cwd=self.cwd,
            env=env,
            shell=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            universal_newlines=True,
        ) as proc:
            with cast(IO[str], proc.stdout):
                for line in cast(IO[str], proc.stdout):
                    print(line, end="")  # noqa: T201
                    output_list.append(line)
            # strip any ANSI escape sequences from output
            output = ANSI_ESCAPE_PATTERN.sub("", "".join(output_list))
            if proc.wait(timeout=timeout) != 0:
                raise subprocess.CalledProcessError(
                    returncode=proc.returncode,
                    cmd=command,
                    output=output,
                    stderr=output,
                )
            return output
