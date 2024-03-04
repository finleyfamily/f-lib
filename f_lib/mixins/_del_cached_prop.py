"""Delete cached property mixin."""

from __future__ import annotations

from contextlib import suppress


class DelCachedPropMixin:
    """Mixin to handle safely clearing the value of :func:`functools.cached_property`."""

    def _del_cached_property(self, *names: str) -> None:
        """Delete the cached value of a :func:`functools.cached_property`.

        Args:
            names: Names of the attribute that is cached. Can provide one or multiple.

        """
        for name in names:
            with suppress(AttributeError):
                delattr(self, name)
