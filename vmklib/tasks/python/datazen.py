"""
A module for datazen tasks.
"""

# built-in
from pathlib import Path
from typing import Dict

# third-party
from vcorelib.task import Inbox, Outbox
from vcorelib.task.manager import TaskManager
from vcorelib.task.subprocess.run import SubprocessLogMixin

# internal
from vmklib.tasks.args import environ_fallback, environ_fallback_split
from vmklib.tasks.python import PREFIX


class DatazenTask(SubprocessLogMixin):
    """A task for running datazen commands."""

    default_requirements = {"venv", PREFIX + "install-datazen"}

    async def run(self, inbox: Inbox, outbox: Outbox, *args, **kwargs) -> bool:
        """Create or update a project's virtual environment."""

        cwd: Path = args[0]

        dz_args = [
            "-C",
            str(cwd),
            "-m",
            environ_fallback("DZ_MANIFEST", "manifest.yaml", **kwargs),
        ]

        return await self.exec(
            str(inbox["venv"]["venv{python_version}"]["python"]),
            "-m",
            "datazen",
            *dz_args,
            *args[1:],
            *environ_fallback_split("DZ_EXTRA_ARGS", **kwargs),
            *environ_fallback_split("DZ_TARGETS", **kwargs),
        )


def register(
    manager: TaskManager,
    project: str,
    cwd: Path,
    substitutions: Dict[str, str],
) -> bool:
    """Register datazen tasks to the manager."""

    manager.register(DatazenTask("dz-sync", cwd), [])
    del project
    del substitutions
    return True
