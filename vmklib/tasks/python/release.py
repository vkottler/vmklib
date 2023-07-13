"""
A module implementing a release task for Python projects.
"""

# built-in
from pathlib import Path
from typing import Dict

# third-party
from vcorelib.task.manager import TaskManager

# internal
from vmklib.tasks.python import PREFIX
from vmklib.tasks.release import GithubRelease


def register(
    manager: TaskManager,
    project: str,
    cwd: Path,
    substitutions: Dict[str, str],
) -> bool:
    """Register Python package tasks to the manager."""

    del project
    del substitutions

    manager.register(
        GithubRelease(PREFIX + "release", cwd),
        ["vmklib.init", PREFIX + "build-once"],
    )

    return True
