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

# internal
from vmklib.tasks.args import environ_fallback_split


class PythonLinter(SubprocessLogMixin):
    """A task for running a Python linter."""

    default_requirements = {"venv"}

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
        linter: str = kwargs["linter"]

        return await self.exec(
            str(inbox["venv"]["venv{python_version}"]["bin"].joinpath(linter)),
            *args[2:],
            # Get extra arguments from the environment.
            *environ_fallback_split(
                "PY_LINT_" + linter.upper() + "_EXTRA_ARGS", **kwargs
            ),
            *PythonLinter.source_args(cwd, project, **kwargs),
        ) or kwargs.get("ignore_errors", False)


def register(
    manager: TaskManager,
    project: str,
    cwd: Path,
    substitutions: Dict[str, str],
) -> bool:
    """Register Python linting tasks to the manager."""

    manager.register(PythonLinter("python-lint-{linter}", cwd, project), [])

    line_length = ["--line-length", str(substitutions.get("line_length", 79))]

    isort_args = line_length + [
        "--profile",
        substitutions.get("isort_profile", "black"),
        "--fss",
        "-m",
        "3",
    ]

    manager.register(
        PythonLinter(
            "python-format-check-isort",
            cwd,
            project,
            "--check-only",
            *isort_args,
            linter="isort",
        ),
        [],
    )

    manager.register(
        PythonLinter(
            "python-format-isort",
            cwd,
            project,
            *isort_args,
            linter="isort",
        ),
        [],
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
        [],
    )

    manager.register(
        PythonLinter(
            "python-format-black",
            cwd,
            project,
            *line_length,
            linter="black",
        ),
        # Depend on 'isort' so that we don't format multiple files at the same
        # time.
        ["python-format-isort"],
    )

    manager.register(
        Phony("python-format-check"),
        ["python-format-check-black", "python-format-check-isort"],
    )
    manager.register(
        Phony("python-format"),
        # 'black' depends on 'isort' already.
        ["python-format-black"],
    )
    manager.register(
        Phony("python-lint"),
        [
            "python-lint-flake8",
            "python-lint-pylint",
            "python-format-check",
        ],
    )

    return True
