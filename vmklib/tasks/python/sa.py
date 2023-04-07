"""
A module for Python static-analysis tasks.
"""

# built-in
from pathlib import Path
from typing import Dict

# third-party
from vcorelib.task import Phony
from vcorelib.task.manager import TaskManager

# internal
from vmklib.tasks.python import PREFIX
from vmklib.tasks.python.lint import PythonLinter


def register(
    manager: TaskManager,
    project: str,
    cwd: Path,
    substitutions: Dict[str, str],
) -> bool:
    """Register static-analysis tasks to the manager."""

    manager.register(Phony(PREFIX + "sa"), [PREFIX + "lint-mypy"])

    # Register a target so that mypy can run without causing an error.
    manager.register(
        PythonLinter(
            PREFIX + "sa-types-init",
            cwd,
            project,
            ignore_errors=True,
            linter="mypy",
        ),
        [PREFIX + "install-mypy"],
    )
    manager.register(
        PythonLinter(
            PREFIX + "sa-types",
            cwd,
            project,
            "--install-types",
            "--non-interactive",
            python_lint_source_args=False,
            linter="mypy",
        ),
        [PREFIX + "sa-types-init"],
    )

    del substitutions
    return True
