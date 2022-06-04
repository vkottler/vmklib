"""
A module for Python-package building tasks.
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
from vmklib.tasks.mixins.concrete import ConcreteBuilderMixin


class PythonBuild(ConcreteBuilderMixin, SubprocessLogMixin):
    """Build a Python package."""

    async def run(
        self,
        inbox: Inbox,
        outbox: Outbox,
        *args,
        **kwargs,
    ) -> bool:
        """TODO."""

        cwd: Path = args[0]

        self.stack.enter_context(in_dir(cwd))

        # Clean directories.
        # * $($(PROJ)_DIR)/dist
        # * $(BUILD_DIR)/bdist*
        # * $(BUILD_DIR)/lib

        # Build package:
        # 'python -m build' inside the project directory

        return True


def register(
    manager: TaskManager,
    project: str,
    cwd: Path,
    substitutions: Dict[str, str],
) -> bool:
    """Register package building tasks to the manager."""

    # Make sure 'wheel' is also installed so we can build a wheel.
    reqs = ["venv", "python-install-wheel", "python-install-build"]
    manager.register(PythonBuild("python-build", cwd, once=False), reqs)
    manager.register(PythonBuild("python-build-once", cwd), reqs)

    del project
    del substitutions
    return True
