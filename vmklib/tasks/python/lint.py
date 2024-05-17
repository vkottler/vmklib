"""
A module for registering Python linting tasks.
"""

# built-in
from pathlib import Path
from typing import Dict, List

# third-party
from vcorelib.platform import is_windows
from vcorelib.task import Inbox, Outbox, Phony
from vcorelib.task.manager import TaskManager
from vcorelib.task.subprocess.run import SubprocessLogMixin

# internal
from vmklib.tasks.args import environ_fallback_split
from vmklib.tasks.python import PREFIX


class PythonLinter(SubprocessLogMixin):
    """A task for running a Python linter."""

    default_requirements = {"venv"}
    linter_args: dict[str, list[str]] = {"ruff": ["check"]}

    @staticmethod
    def source_args(cwd: Path, project: str, **kwargs) -> List[str]:
        """Get Python sources within a package."""

        sources = []
        if kwargs.get("python_lint_source_args", True):
            sources = [
                cwd.joinpath("tests"),
                cwd.joinpath(project),
                cwd.joinpath("setup.py"),
            ]

            # This breaks on Windows because of symbolic linking. It's okay
            # to lose the linting coverage for the not-unit-tested workflow
            # code.
            if not is_windows():
                sources.append(cwd.joinpath("tasks"))

        return list(str(x) for x in filter(lambda x: x.exists(), sources))

    async def run(self, inbox: Inbox, outbox: Outbox, *args, **kwargs) -> bool:
        """Run a Python linter."""

        cwd: Path = args[0]
        project: str = args[1]
        linter: str = kwargs.get("package", kwargs.get("linter", "UNKNOWN"))

        return await self.exec(
            str(inbox["venv"]["venv{python_version}"]["bin"].joinpath(linter)),
            *self.linter_args.get(linter, []),
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

    prefix = PREFIX

    # A target ensuring that linter packages are installed.
    for kind in ["install", "upgrade"]:
        manager.register(
            Phony(prefix + f"lint-{kind}"),
            [
                f"{prefix}{kind}-{x}"
                for x in ["pylint", "flake8", "black", "ruff", "mypy", "isort"]
            ],
        )

    manager.register(
        PythonLinter(prefix + "lint-{package}", cwd, project),
        [prefix + "install-{package}"],
    )

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
            prefix + "format-check-isort",
            cwd,
            project,
            "--check-only",
            *isort_args,
            linter="isort",
        ),
        [f"{prefix}install-isort"],
    )

    manager.register(
        PythonLinter(
            prefix + "format-isort",
            cwd,
            project,
            *isort_args,
            linter="isort",
        ),
        [f"{prefix}install-isort"],
    )

    manager.register(
        PythonLinter(
            prefix + "format-check-black",
            cwd,
            project,
            "--check",
            *line_length,
            linter="black",
        ),
        [f"{prefix}install-black"],
    )

    manager.register(
        PythonLinter(
            prefix + "format-black",
            cwd,
            project,
            *line_length,
            linter="black",
        ),
        # Depend on 'isort' so that we don't format multiple files at the same
        # time.
        [f"{prefix}install-black", prefix + "format-isort"],
    )

    manager.register(
        Phony(prefix + "format-check"),
        [prefix + "format-check-black", prefix + "format-check-isort"],
    )
    manager.register(
        Phony(prefix + "format"),
        # 'black' depends on 'isort' already.
        [prefix + "format-black"],
    )
    manager.register(
        Phony(prefix + "lint"),
        [
            prefix + "lint-flake8",
            prefix + "lint-pylint",
            prefix + "lint-ruff",
            prefix + "format-check",
        ],
    )

    return True
