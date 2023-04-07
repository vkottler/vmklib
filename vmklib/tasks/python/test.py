"""
A module for Python unit testing tasks.
"""

# built-in
from pathlib import Path
from typing import Dict

# third-party
from vcorelib.task import Inbox, Outbox
from vcorelib.task.manager import TaskManager
from vcorelib.task.subprocess.run import SubprocessLogMixin

# internal
from vmklib.tasks.args import environ_fallback_split
from vmklib.tasks.python import PREFIX


class PythonTester(SubprocessLogMixin):
    """A task for running pytest."""

    default_requirements = {"venv"}

    async def run(self, inbox: Inbox, outbox: Outbox, *args, **kwargs) -> bool:
        """Run pytest against the project."""

        cwd: Path = args[0]
        project: str = args[1]
        tester = kwargs.get("tester", "pytest")
        pattern = kwargs.get("pattern")

        test_args = [
            "-x",
            f"--log-cli-level={kwargs.get('log_level', 10)}",
            f"--cov={project}",
            "--cov-report",
            "html",
        ]
        if pattern is not None:
            test_args.append("-k")
            test_args.append(pattern)

        return await self.exec(
            str(inbox["venv"]["venv{python_version}"]["bin"].joinpath(tester)),
            *test_args,
            *environ_fallback_split("PY_TEST_EXTRA_ARGS", **kwargs),
            str(cwd.joinpath("tests")),
        )


def register(
    manager: TaskManager,
    project: str,
    cwd: Path,
    substitutions: Dict[str, str],
) -> bool:
    """Register unit testing tasks to the manager."""

    # Packages to install for running unit tests.
    deps = [f"{PREFIX}install-{x}" for x in ["pytest", "pytest-cov"]]

    manager.register(
        PythonTester(PREFIX + "test", cwd, project),
        deps,
    )
    manager.register(
        PythonTester(PREFIX + "test-{pattern}", cwd, project), deps
    )
    del substitutions
    return True
