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
            kwargs.get("PY_DEPS_OUT", str(images.joinpath("pydeps.svg"))),
            *kwargs.get("PY_DEPS_EXTRA_ARGS", "").split(),
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
