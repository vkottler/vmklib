"""
A module for project-specific task registration.
"""

# built-in
from pathlib import Path
from typing import Dict

# third-party
from vcorelib.task import Phony
from vcorelib.task.manager import TaskManager


def register(
    manager: TaskManager,
    project: str,
    cwd: Path,
    substitutions: Dict[str, str],
) -> bool:
    """Register project tasks to the manager."""

    manager.register(
        Phony("yaml"), ["yaml-lint-local", "yaml-lint-manifest.yaml"]
    )
    del project
    del cwd
    del substitutions
    return True
