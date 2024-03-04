"""Constants."""

import re

ANSI_ESCAPE_PATTERN = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
"""Pattern to match ANSI escape sequences."""
