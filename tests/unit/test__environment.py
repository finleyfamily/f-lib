"""Test f_lib._environment."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from f_lib._environment import Environment

if TYPE_CHECKING:
    from pathlib import Path

MODULE = "f_lib._environment"


class TestEnvironment:
    """Test Environment."""

    def test___bool__(self, tmp_path: Path) -> None:
        """Test __bool__."""
        assert Environment(environ={"key": "value"}, root_dir=tmp_path)

    def test___bool___false(self, tmp_path: Path) -> None:
        """Test __bool__ is ``False``."""
        assert not Environment(environ={}, root_dir=tmp_path)

    def test___eq__(self, tmp_path: Path) -> None:
        """Test __eq__."""
        assert Environment(environ={"key": "value"}, root_dir=tmp_path) == Environment(
            environ={"key": "value"}, root_dir=tmp_path
        )

    def test___eq___false_environ(self, tmp_path: Path) -> None:
        """Test __eq__ is ``False``."""
        assert not Environment(  # noqa: SIM201
            environ={"key": "value"}, root_dir=tmp_path
        ) == Environment(environ={"foo": "bar"}, root_dir=tmp_path)

    def test___eq___false_root_dir(self, tmp_path: Path) -> None:
        """Test __eq__ is ``False``."""
        assert not Environment(  # noqa: SIM201
            environ={"key": "value"}, root_dir=tmp_path
        ) == Environment(environ={"key": "value"}, root_dir=tmp_path / "child")

    def test___eq___not_implemented(self, tmp_path: Path) -> None:
        """Test __eq__ ``NotImplemented``."""
        assert not Environment(environ={"key": "value"}, root_dir=tmp_path) == {  # noqa: SIM201
            "key": "value"
        }

    def test___hash__(self, tmp_path: Path) -> None:
        """Test __hash__."""
        obj = Environment(environ={"key": "value"}, root_dir=tmp_path)
        assert isinstance(hash(obj), int)

        # Ensure that the hash is consistent
        assert hash(obj) == hash(obj)

    def test___init__(self, cd_tmp_path: Path) -> None:
        """Test attributes set by init."""
        new_dir = cd_tmp_path / "new_dir"
        obj = Environment(
            environ={"key": "val"},
            root_dir=new_dir,
        )

        assert obj.root_dir == new_dir
        assert obj.vars == {"key": "val"}

    def test___init___defaults(self, cd_tmp_path: Path) -> None:
        """Test attributes set by init default values."""
        obj = Environment()

        assert obj.root_dir == cd_tmp_path
        assert obj.vars == os.environ

    def test___init___emptry_environ(self) -> None:
        """Test attributes set by init."""
        assert Environment(environ={}).vars == {}

    def test___ne___environ(self, tmp_path: Path) -> None:
        """Test __ne__."""
        assert Environment(environ={"key": "value"}, root_dir=tmp_path) != Environment(
            environ={"foo": "bar"}, root_dir=tmp_path
        )

    def test___ne___false(self, tmp_path: Path) -> None:
        """Test __ne__ is ``False``."""
        assert not Environment(  # noqa: SIM202
            environ={"key": "value"}, root_dir=tmp_path
        ) != Environment(environ={"key": "value"}, root_dir=tmp_path)

    def test___ne___root_dir(self, tmp_path: Path) -> None:
        """Test __ne__ is."""
        assert Environment(environ={"key": "value"}, root_dir=tmp_path) != Environment(
            environ={"key": "value"}, root_dir=tmp_path / "child"
        )

    def test___ne___not_implemented(self, tmp_path: Path) -> None:
        """Test __ne__ ``NotImplemented``."""
        assert Environment(environ={"key": "value"}, root_dir=tmp_path) != {"key": "value"}

    def test_ci_deleter(self) -> None:
        """Test ``@ci.deleter``."""
        obj = Environment(environ={"CI": "1"})
        del obj.ci
        assert not obj.ci
        assert "CI" not in obj.vars

    def test_ci_setter(self) -> None:
        """Test ``@ci.setter``."""
        obj = Environment(environ={})
        obj.ci = True
        assert obj.ci
        assert obj.vars["CI"] == "1"

        obj.ci = False
        assert not obj.ci
        assert "CI" not in obj.vars

    def test_ci_unset(self) -> None:
        """Test ci."""
        assert not Environment(environ={}).ci

    def test_copy(self, tmp_path: Path) -> None:
        """Test copy."""
        obj = Environment(root_dir=tmp_path)
        obj_copy = obj.copy()

        assert id(obj_copy) != id(obj)
        assert obj_copy.root_dir == obj.root_dir
        assert obj_copy.vars == obj.vars

    def test_debug_setter(self) -> None:
        """Test ``@debug.setter``."""
        obj = Environment(environ={})
        obj.debug = True
        assert obj.debug
        assert obj.vars["DEBUG"] == "1"

        obj.debug = False
        assert not obj.debug
        assert "DEBUG" not in obj.vars

    def test_debug_unset(self) -> None:
        """Test debug."""
        assert not Environment(environ={}).debug

    def test_verbose_setter(self) -> None:
        """Test ``@verbose.setter``."""
        obj = Environment(environ={})
        obj.verbose = True
        assert obj.verbose
        assert obj.vars["VERBOSE"] == "1"

        obj.verbose = False
        assert not obj.verbose
        assert "VERBOSE" not in obj.vars

    def test_verbose_unset(self) -> None:
        """Test verbose."""
        assert not Environment(environ={}).verbose
