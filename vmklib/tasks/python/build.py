"""
A module for Python-package building tasks.
"""

# built-in
from pathlib import Path
from typing import Dict

# third-party
from vcorelib.task.manager import TaskManager
from vcorelib.task.subprocess.run import SubprocessLogMixin


class PythonBuild(SubprocessLogMixin):
    """Build a Python package."""

    # Clean build, remove:
    # * $($(PROJ)_DIR)/dist
    # * $(BUILD_DIR)/bdist*
    # * $(BUILD_DIR)/lib

    # Build package:
    # 'python -m build' inside the project directory

    # for changing directories, we need some kind of concurrency safety
    # probably

    # Allow a 'build-once' target variant


def register(
    manager: TaskManager,
    project: str,
    cwd: Path,
    substitutions: Dict[str, str],
) -> bool:
    """Register package building tasks to the manager."""

    # Make sure 'wheel' is also installed so we can build a wheel.
    reqs = ["venv", "python-install-wheel", "python-install-build"]

    manager.register(PythonBuild("python-build"), reqs)

    manager.register(PythonBuild("python-build-once", once=True), reqs)

    del project
    del cwd
    del substitutions
    return True
