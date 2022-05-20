"""
A module for registering package tasks.
"""

# built-in
from os import environ
from pathlib import Path
from platform import system
from sys import version_info

from vcorelib.task.dict.melder import DictMerger

# third-party
from vcorelib.task.manager import TaskManager


def python_version() -> str:
    """Get the version of Python to use."""
    return environ.get(
        "PYTHON_VERSION", f"{version_info[0]}.{version_info[1]}"
    )


def venv_name() -> str:
    """Get the name for a virtual environment to use."""
    return f"venv{python_version()}"


def venv_dir(cwd: Path) -> Path:
    """Get the path for a virtual environment to use."""
    return cwd.joinpath(venv_name())


def venv_bin(cwd: Path, program: str = None) -> Path:
    """Get the path to a virtual environment's script directory."""

    path = venv_dir(cwd).joinpath(
        "bin" if not system() == "Windows" else "Scripts"
    )
    if program is not None:
        path = path.joinpath(program)
    return path


def register(manager: TaskManager, project: str, cwd: Path, **kwargs) -> bool:
    """Register package tasks to the manager."""

    # Set up initial data so that every task has easy access to common
    # definitions.
    init_data = {
        "__dirs__": {
            "build": cwd.joinpath("build"),
            "venv": venv_dir(cwd),
            "venv_bin": venv_bin(cwd),
            "proj": cwd.joinpath(project),
        },
        "__files__": {"python": venv_bin(cwd, "python")},
    }

    # Register the initialization task.
    manager.register(DictMerger("vmklib.init", {**kwargs}, init_data))
    return True
