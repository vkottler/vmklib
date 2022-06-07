"""
Utilities for working with Python.
"""

# built-in
from os import environ
from pathlib import Path
from sys import base_prefix, executable, prefix, version_info

# third-party
from vcorelib.task.subprocess.run import is_windows


def python_version() -> str:
    """Get the version of Python to use."""
    return environ.get(
        "PYTHON_VERSION", f"{version_info[0]}.{version_info[1]}"
    )


def in_venv() -> bool:
    """A simple way to check if we're in a virtual environment."""
    return prefix != base_prefix


def python_entry(version: str) -> str:
    """Attempt to get a Python entry-point as a string."""

    # If the provided version is compatible with the current executable,
    # return that. If not, try to return something that might be found by
    # the interpreter.
    return (
        str(executable)
        if version.startswith(f"{version_info[0]}.{version_info[1]}")
        # Don't allow this executable promotion if we're already in a virtual
        # environment. Always allow this promotion on Windows because Windows
        # may not have 'pythonX.Y.exe' executables available.
        and (not in_venv() or is_windows())
        else f"python{version}{'.exe' if is_windows() else ''}"
    )


def venv_name(version: str = None) -> str:
    """Get the name for a virtual environment to use."""
    if version is None:
        version = python_version()
    return f"venv{version}"


def venv_dir(cwd: Path, version: str = None) -> Path:
    """Get the path for a virtual environment to use."""
    return cwd.joinpath(venv_name(version))


def venv_bin(cwd: Path, program: str = None, version: str = None) -> Path:
    """Get the path to a virtual environment's script directory."""

    path = venv_dir(cwd, version).joinpath(
        "Scripts" if is_windows() else "bin"
    )
    if program is not None:
        path = path.joinpath(f"{program}{'.exe' if is_windows() else ''}")
    return path
