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
from vmklib.tasks.python import PREFIX


class PydepsTask(SubprocessLogMixin):
    """A task for running pydeps."""

    default_requirements = {"venv", PREFIX + "install-pydeps"}

    async def run(self, inbox: Inbox, outbox: Outbox, *args, **kwargs) -> bool:
        """Create or update a project's virtual environment."""

        cwd: Path = args[0]
        project: str = args[1]
        self.stack.enter_context(in_dir(cwd))

        # Create 'im'.
        images = Path("im")
        images.mkdir(parents=True, exist_ok=True)

        output = Path(
            environ_fallback(
                "PY_DEPS_OUT", str(images.joinpath("pydeps.svg")), **kwargs
            )
        )

        return (
            await self.exec(
                str(inbox["venv"]["venv{python_version}"]["python"]),
                "-m",
                "pydeps",
                "--no-show",
                "-T",
                "svg",
                "-o",
                str(output),
                *environ_fallback_split("PY_DEPS_EXTRA_ARGS", **kwargs),
                project,
            )
            # Only generate the output if it's missing (this is time-consuming
            # to run).
            if not output.is_file()
            else True
        )


def register(
    manager: TaskManager,
    project: str,
    cwd: Path,
    substitutions: Dict[str, str],
) -> bool:
    """Register documentation tasks to the manager."""

    manager.register(PydepsTask(PREFIX + "deps", cwd, project), [])
    del substitutions
    return True
