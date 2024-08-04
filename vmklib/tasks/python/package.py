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
from vmklib.util import to_slug


class PythonPackage(ConcreteOnceMixin, SubprocessLogMixin):
    """A task for installing a single Python package."""

    default_requirements = {"venv", "vmklib.init"}

    async def run(self, inbox: Inbox, outbox: Outbox, *args, **kwargs) -> bool:
        """Create or update a project's virtual environment."""

        install_args = [*args]

        to_install = kwargs["package"]
        project = kwargs.get("project")

        # Perform an editable install if we're the install target.
        if project and to_slug(project) == to_slug(to_install):
            install_args.append("-e")
            to_install = "."

        install_args.append(to_install)

        return await self.exec(
            str(inbox["venv"]["venv{python_version}"]["pip"]),
            "install",
            *install_args,
        )


def register(
    manager: TaskManager,
    project: str,
    cwd: Path,
    substitutions: Dict[str, str],
) -> bool:
    """Register Python package tasks to the manager."""

    del cwd
    del substitutions

    # A target that installs a package.
    manager.register(
        PythonPackage(
            "python{python_version}-install-{package}", project=project
        ),
        [],
    )

    # A target that attempts to upgrade a package.
    manager.register(
        PythonPackage(
            "python{python_version}-upgrade-{package}",
            "--upgrade",
            once=False,
            project=project,
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
