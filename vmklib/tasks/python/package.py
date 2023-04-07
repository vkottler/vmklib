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
from vmklib.tasks.python import PREFIX


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

    # A target that installs a package.
    manager.register(
        PythonPackage("python{python_version}-install-{package}"), []
    )

    # A target that attempts to upgrade a package.
    manager.register(
        PythonPackage(
            "python{python_version}-upgrade-{package}", "--upgrade", once=False
        ),
        [],
    )

    # Less verbose phony front-ends to package installation and upgrading.
    manager.register(
        Phony(PREFIX + "install-{package}"),
        ["python{python_version}-install-{package}"],
    )
    manager.register(
        Phony(PREFIX + "upgrade-{package}"),
        ["python{python_version}-upgrade-{package}"],
    )

    manager.register(PythonPackage(PREFIX + "editable", "-e", package="."), [])
    return True
