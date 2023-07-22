"""
Utilities for working with Python.
"""

# third-party
from vcorelib.python import (
    python_entry,
    python_version,
    venv_bin,
    venv_dir,
    venv_name,
)

PREFIX = "python-"
__all__ = [
    "PREFIX",
    "python_version",
    "python_entry",
    "venv_name",
    "venv_dir",
    "venv_bin",
]
