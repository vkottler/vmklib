"""
A module implementing a task for installing individual packages.
"""

# built-in
from pathlib import Path
from typing import Dict

# third-party
from vcorelib.task import Inbox, Outbox, Phony
from vcorelib.task.manager import TaskManager
from vcorelib.task.subprocess.run import SubprocessLogMixin

# internal
from vmklib.tasks.mixins.concrete import ConcreteOnceMixin


class PythonPackage(ConcreteOnceMixin, SubprocessLogMixin):
    """A task for installing a single Python package."""

    default_requirements = {"venv", "vmklib.init"}

    async def run(self, inbox: Inbox, outbox: Outbox, *args, **kwargs) -> bool:
        """Create or update a project's virtual environment."""

        return await self.exec(
            str(inbox["venv"]["venv{python_version}"]["pip"]),
            "install",
            *args,
            kwargs["package"],
        )


def register(
    manager: TaskManager,
    project: str,
    cwd: Path,
    substitutions: Dict[str, str],
) -> bool:
    """Register Python package tasks to the manager."""

    del project
    del cwd
    del substitutions
    manager.register(
        PythonPackage("python{python_version}-install-{package}"), []
    )
    manager.register(
        Phony("python-install-{package}"),
        ["python{python_version}-install-{package}"],
    )
    manager.register(PythonPackage("python-editable", "-e", package="."), [])
    return True
