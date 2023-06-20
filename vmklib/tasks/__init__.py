"""
A module implementing a base task.
"""

# built-in
from pathlib import Path
from typing import cast

# third-party
from vcorelib.task import Inbox, Task


class VmklibBase(Task):
    """Create a concrete file output after a task completes."""

    default_requirements = {"vmklib.init"}

    @classmethod
    def build_dir(cls, inbox: Inbox) -> Path:
        """Get a path to the build directory."""
        return cast(Path, inbox["vmklib.init"]["__dirs__"]["build"])
