"""
A module for registering virtual environment tasks.
"""

# built-in
from pathlib import Path
from typing import Dict

# third-party
from vcorelib.dict import set_if_not
from vcorelib.task import Inbox, Outbox, Phony
from vcorelib.task.manager import TaskManager
from vcorelib.task.subprocess.run import SubprocessLogMixin

# internal
from vmklib.tasks.mixins.concrete import ConcreteBuilderMixin
from vmklib.tasks.python import PREFIX, python_entry
from vmklib.tasks.python import python_version as _python_version
from vmklib.tasks.python import venv_bin, venv_dir


class Venv(ConcreteBuilderMixin, SubprocessLogMixin):
    """A target prototype for creating a virtual environment."""

    async def run_enter(
        self,
        _inbox: Inbox,
        _outbox: Outbox,
        *_args,
        **_kwargs,
    ) -> bool:
        """
        Check if the virtual environment gets created and expose useful data
        to the outbox.
        """

        cwd: Path = _args[0]
        python_version = _kwargs.get("python_version", _python_version())
        path = venv_dir(cwd, python_version)

        # If the environment already exists we don't need to create it.
        python = venv_bin(cwd, "python", python_version)
        if path.is_dir() and python.is_file():
            self._continue = False
            self.update_concrete(_inbox, **_kwargs)

        # Set the path in the outbox so we can easily find it.
        _outbox["path"] = path
        _outbox["bin"] = venv_bin(cwd, None, python_version)
        _outbox["python"] = python
        _outbox["pip"] = venv_bin(cwd, "pip", python_version)
        return True

    async def run(self, inbox: Inbox, outbox: Outbox, *args, **kwargs) -> bool:
        """Create or update a project's virtual environment."""

        result = True

        # Run the command.
        result = await self.exec(
            python_entry(kwargs.get("python_version", _python_version())),
            "-m",
            "venv",
            str(outbox["path"]),
        )

        # Upgrade pip by default.
        if result and kwargs.get("upgrade_pip", True):
            result = await self.exec(
                str(outbox["python"]),
                "-m",
                "pip",
                "install",
                "--upgrade",
                "pip",
            )

        # Install 'wheel' by default. Use the 'pip' script directly to sanity
        # check that the actual virtual environment has pip.
        if result:
            result = await self.exec(
                str(outbox["pip"]),
                "install",
                "--upgrade",
                "wheel",
            )

        return result


class RequirementsInstaller(ConcreteBuilderMixin, SubprocessLogMixin):
    """A task for installing requirements files."""

    async def run(self, inbox: Inbox, outbox: Outbox, *args, **kwargs) -> bool:
        """Install a requirements file."""

        result = True

        # Only take action if any of the requirements are newer than the
        # concrete.
        req_files = [*args]
        self._continue = self.is_concrete_stale(inbox, req_files, {**kwargs})
        if self._continue:
            for req in req_files:
                if result:
                    # Run the command.
                    result = await self.exec(
                        str(inbox["venv{python_version}"]["python"]),
                        "-m",
                        "pip",
                        "install",
                        "-r",
                        str(req),
                    )

        return result


def register(
    manager: TaskManager,
    project: str,
    cwd: Path,
    substitutions: Dict[str, str],
) -> bool:
    """Register virtual environment tasks to the manager."""

    # Ensure that a valid version is set.
    set_if_not(substitutions, "python_version", _python_version())

    # The target that actually creates the initial environment.
    manager.register(Venv("venv{python_version}", cwd), [])

    # Add a "phony" style target to just create the virtual environment. Here
    # We would also add dependencies like requirement-file installs.
    manager.register(Phony("venv"), ["venv{python_version}"])

    # Look for requirements files.
    requirements_files = [
        cwd.joinpath("requirements.txt"),
        cwd.joinpath("dev_requirements.txt"),
        cwd.joinpath(project, "requirements.txt"),
        cwd.joinpath(project, "dev_requirements.txt"),
    ]

    # Register requirements' install tasks.
    manager.register(
        RequirementsInstaller(
            "python{python_version}-project-requirements",
            *list(filter(lambda x: x.is_file(), requirements_files)),
        ),
        ["vmklib.init", "venv{python_version}"],
    )
    manager.register(
        Phony(PREFIX + "project-requirements"),
        ["python{python_version}-project-requirements"],
    )
    manager.register_to("venv", [PREFIX + "project-requirements"])

    return True
