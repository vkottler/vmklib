"""
A task mixin for writing concrete outputs to a build directory.
"""

# built-in
from os import linesep
from pathlib import Path
from time import asctime
from typing import Iterable

# third-party
from vcorelib.paths import Pathlike, modified_after
from vcorelib.target import Substitutions
from vcorelib.task import Inbox, Outbox

# internal
from vmklib.tasks import VmklibBase


class ConcreteBuilderMixin(VmklibBase):
    """Create a concrete file output after a task completes."""

    def concrete_path(
        self,
        inbox: Inbox,
        substitutions: Substitutions = None,
    ) -> Path:
        """By default name the concrete after the compiled target name."""

        return self.build_dir(inbox).joinpath(
            f"{self.target.compile(substitutions)}.txt"
        )

    def is_concrete_stale(
        self,
        inbox: Inbox,
        candidates: Iterable[Pathlike],
        substitutions: Substitutions = None,
    ) -> bool:
        """Check if any candidate paths are modified after the concrete was."""

        return modified_after(
            self.concrete_path(inbox, substitutions), candidates
        )

    def update_concrete(self, inbox: Inbox, **kwargs) -> Path:
        """
        Write a text file to disk in the build directory based on the name of
        this task.

        This is useful to bootstrap compatibility with other tools like GNU
        Make that assess concrete targets.
        """

        concrete = self.concrete_path(inbox, {**kwargs})

        # Write data to the concrete file.
        concrete.parent.mkdir(parents=True, exist_ok=True)
        with concrete.open("w", encoding="utf-8") as concrete_fd:
            concrete_fd.write(asctime())
            concrete_fd.write(linesep)
        return concrete

    async def run_exit(
        self, _inbox: Inbox, _outbox: Outbox, *_args, **kwargs
    ) -> bool:
        """Update the concrete target after main execution by default."""

        _outbox["concrete"] = self.update_concrete(_inbox, **kwargs)
        return True


class ConcreteOnceMixin(ConcreteBuilderMixin):
    """A mixin for tasks that only need to run once."""

    async def run_enter(
        self,
        _inbox: Inbox,
        _outbox: Outbox,
        *_args,
        **_kwargs,
    ) -> bool:
        """Ensure that this task only runs once."""

        if _kwargs.get("once", True):
            if self.concrete_path(_inbox, {**_kwargs}).exists():
                self._continue = False

        return True
