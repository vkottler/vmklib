"""
Utilities for working with Python.
"""

# built-in
from os import environ
from pathlib import Path
from shutil import which
from sys import executable, version_info

# third-party
from vcorelib.task.subprocess.run import is_windows


def python_version() -> str:
    """Get the version of Python to use."""
    return environ.get(
        "PYTHON_VERSION", f"{version_info[0]}.{version_info[1]}"
    )


def python_entry(version: str) -> str:
    """Attempt to get a Python entry-point as a string."""

    result = None

    options = [f"python{version}{'.exe' if is_windows() else ''}"]

    # Use the current executable as a candidate if it's the right version.
    if version.startswith(f"{version_info[0]}.{version_info[1]}"):
        result = str(executable)
        options.append(result)

    for option in options:
        if which(option) is not None:
            result = option
            break

    assert result is not None, f"Couldn't find 'python{version}'!"
    return result


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
