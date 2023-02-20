"""
Task implementations for working with node.js.
"""

# built-in
from pathlib import Path
from typing import Dict

# third-party
from vcorelib.task import Inbox, Outbox, Phony
from vcorelib.task.manager import TaskManager
from vcorelib.task.subprocess.run import SubprocessLogMixin

PREFIX = "node-"


class Npx(SubprocessLogMixin):
    """A task that runs npx."""

    async def run(self, inbox: Inbox, outbox: Outbox, *args, **kwargs) -> bool:
        """Run command."""
        return await self.exec("npx", *args)


def register(
    manager: TaskManager,
    project: str,
    cwd: Path,
    substitutions: Dict[str, str],
) -> bool:
    """Register node.js project tasks to the manager."""

    del project
    del substitutions

    src = str(cwd.joinpath("src"))
    tests = str(cwd.joinpath("tests"))

    # Project tasks.
    manager.register(Npx(PREFIX + "build", "parcel", "build"))
    manager.register(Npx(PREFIX + "host", "parcel", "--no-cache"))

    # Formatting.
    manager.register(Npx("eslint-format", "eslint", "--fix", src, tests))
    manager.register(Npx("prettier-format", "prettier", "-w", src, tests))
    manager.register(
        Phony(PREFIX + "format"), ["eslint-format", "prettier-format"]
    )

    # Linting.
    manager.register(Npx("eslint-lint", "eslint", src, tests))
    manager.register(Npx("prettier-lint", "prettier", "--check", src, tests))
    manager.register(Phony(PREFIX + "lint"), ["eslint-lint", "prettier-lint"])

    # Testing.
    manager.register(Npx(PREFIX + "test", "jest", "--coverage"))
    return True
