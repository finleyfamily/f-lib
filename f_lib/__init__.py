"""Import modules."""
import sys

if sys.version_info[1] < 8:
    # importlib.metadata is standard lib for python>=3.8, use backport
    from importlib_metadata import version, PackageNotFoundError
else:
    from importlib.metadata import version, PackageNotFoundError  # pylint: disable=E

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    # package is not installed
    __version__ = '0.0.0'
