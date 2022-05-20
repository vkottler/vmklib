"""
A module for registering project tasks.
"""

# built-in
from pathlib import Path

# third-party
from vcorelib.task.manager import TaskManager


def register(manager: TaskManager, project: str, cwd: Path, **kwargs) -> bool:
    """Register project tasks to the manager."""

    del manager
    del project
    del cwd
    del kwargs
    return True
