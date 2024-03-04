"""Test f_lib.logging._log_level."""

from __future__ import annotations

import pytest

from f_lib.logging._log_level import LogLevel


class TestLogLevel:
    """Test LogLevel."""

    @pytest.mark.parametrize(
        ("verbosity", "level"),
        [
            (0, LogLevel.FATAL),
            (1, LogLevel.INFO),
            (2, LogLevel.VERBOSE),
            (3, LogLevel.DEBUG),
            (4, LogLevel.DEBUG),
            (5, LogLevel.NOTSET),
        ],
    )
    def test_from_verbosity(self, level: LogLevel, verbosity: int) -> None:
        """Test from_verbosity."""
        assert LogLevel.from_verbosity(verbosity) == level

    def test_has_value(self) -> None:
        """Test has_value."""
        assert LogLevel.has_value(20)

    def test_has_value_false(self) -> None:
        """Test has_value False."""
        assert not LogLevel.has_value(9001)
