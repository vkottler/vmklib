"""
A task mixin for writing concrete outputs to a build directory.
"""

# built-in
from os import linesep
from pathlib import Path
from time import asctime
from typing import Dict

# third-party
from vcorelib.task import Inbox, Outbox, Task


class ConcreteBuilderMixin(Task):
    """Create a concrete file output after a task completes."""

    def concrete_path(self, substitutions: Dict[str, str] = None) -> Path:
        """By default name the concrete after the compiled target name."""
        return Path(f"{self.target.compile(substitutions)}.txt")

    def update_concrete(self, inbox: Inbox, **kwargs) -> None:
        """
        Write a text file to disk in the build directory based on the name of
        this task.

        This is useful to bootstrap compatibility with other tools like GNU
        Make that assess concrete targets.
        """

        init_data = inbox["vmklib.init"]
        build = init_data["__dirs__"]["build"]
        substitutions = {**kwargs}
        concrete = build.joinpath(self.concrete_path(substitutions))

        # Write data to the concrete file.
        concrete.parent.mkdir(parents=True, exist_ok=True)
        with concrete.open("w") as concrete_fd:
            concrete_fd.write(asctime())
            concrete_fd.write(linesep)

    async def run_exit(
        self, _inbox: Inbox, _outbox: Outbox, *_args, **kwargs
    ) -> bool:
        """Update the concrete target after main execution by default."""

        self.update_concrete(_inbox, **kwargs)
        return True
