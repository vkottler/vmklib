"""
A module for registering Python linting tasks.
"""

# built-in
from pathlib import Path
from typing import Dict, List

# third-party
from vcorelib.task import Inbox, Outbox, Phony
from vcorelib.task.manager import TaskManager
from vcorelib.task.subprocess.run import SubprocessLogMixin


class PythonLinter(SubprocessLogMixin):
    """A task for running a Python linter."""

    @staticmethod
    def source_args(cwd: Path, project: str, **kwargs) -> List[str]:
        """Get Python sources within a package."""

        sources = []
        if kwargs.get("python_lint_source_args", True):
            sources = [
                cwd.joinpath("tests"),
                cwd.joinpath(project),
                cwd.joinpath("tasks"),
                cwd.joinpath("setup.py"),
            ]
        return list(str(x) for x in filter(lambda x: x.exists(), sources))

    async def run(self, inbox: Inbox, outbox: Outbox, *args, **kwargs) -> bool:
        """Run a Python linter."""

        cwd: Path = args[0]
        project: str = args[1]

        return await self.exec(
            str(
                inbox["venv"]["venv{python_version}"]["bin"].joinpath(
                    kwargs["linter"]
                )
            ),
            *args[2:],
            *PythonLinter.source_args(cwd, project, **kwargs),
        )


def register(
    manager: TaskManager,
    project: str,
    cwd: Path,
    substitutions: Dict[str, str],
) -> bool:
    """Register Python linting tasks to the manager."""

    manager.register(
        PythonLinter("python-lint-{linter}", cwd, project), ["venv"]
    )

    line_length = ["--line-length", str(substitutions.get("line_length", 79))]

    manager.register(
        PythonLinter(
            "python-format-check-isort",
            cwd,
            project,
            "--check-only",
            *line_length,
            "--profile",
            substitutions.get("isort_profile", "black"),
            "--fss",
            "-m",
            "3",
            linter="isort",
        ),
        ["venv"],
    )

    manager.register(
        PythonLinter(
            "python-format-check-black",
            cwd,
            project,
            "--check",
            *line_length,
            linter="black",
        ),
        ["venv"],
    )

    manager.register(
        Phony("python-format-check"),
        ["python-format-check-black", "python-format-check-isort"],
    )
    manager.register(
        Phony("python-lint"),
        ["python-lint-flake8", "python-lint-pylint", "python-format-check"],
    )

    return True
