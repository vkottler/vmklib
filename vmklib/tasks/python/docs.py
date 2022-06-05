"""
A module for Python documentation tasks.
"""

# built-in
from pathlib import Path
from typing import Dict

# third-party
from vcorelib.paths.context import in_dir
from vcorelib.task import Inbox, Outbox
from vcorelib.task.manager import TaskManager
from vcorelib.task.subprocess.run import SubprocessLogMixin

# internal
from vmklib.tasks.args import environ_fallback, environ_fallback_split


class PydepsTask(SubprocessLogMixin):
    """A task for running pydeps."""

    default_requirements = {"venv", "python-install-pydeps"}

    async def run(self, inbox: Inbox, outbox: Outbox, *args, **kwargs) -> bool:
        """Create or update a project's virtual environment."""

        cwd: Path = args[0]
        project: str = args[1]
        self.stack.enter_context(in_dir(cwd))

        # Create 'im'.
        images = Path("im")
        images.mkdir(parents=True, exist_ok=True)

        return await self.exec(
            str(inbox["venv"]["venv{python_version}"]["python"]),
            "-m",
            "pydeps",
            "--no-show",
            "-T",
            "svg",
            "-o",
            environ_fallback(
                "PY_DEPS_OUT", str(images.joinpath("pydeps.svg")), **kwargs
            ),
            *environ_fallback_split("PY_DEPS_EXTRA_ARGS", **kwargs),
            project,
        )


def register(
    manager: TaskManager,
    project: str,
    cwd: Path,
    substitutions: Dict[str, str],
) -> bool:
    """Register documentation tasks to the manager."""

    manager.register(PydepsTask("python-deps", cwd, project), [])
    del substitutions
    return True
