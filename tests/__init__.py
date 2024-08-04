""""
vmklib - Shared test utilities.
"""

# built-in
from contextlib import contextmanager
from pathlib import Path
from shutil import rmtree
import tempfile
from typing import Iterator, List

# module under test
from vmklib import PKG_NAME


@contextmanager
def get_args() -> Iterator[List[str]]:
    """Get command-line arguments for this testing environment."""

    tdir = tempfile.TemporaryDirectory()
    base_args = [PKG_NAME, "-C", tdir.name]
    try:
        yield base_args
    finally:
        tdir.cleanup()


def get_resource(resource_name: str) -> str:
    """Locate the path to a test resource."""
    return str(Path(__file__).parent.joinpath("data", resource_name))


@contextmanager
def build_cleaned_resource(resource_name: str) -> Iterator[str]:
    """
    Get a path to a resourc and ensure that a 'build' directory relative to it
    is cleaned up before and after providing it.
    """

    path = Path(get_resource(resource_name))

    # Try our best to clean up virtual environments.
    to_clean = ["build", "venv"] + [f"venv3.{x}" for x in range(6, 6 + 20)]

    for clean in to_clean:
        clean_path = path.joinpath(clean)
        rmtree(clean_path, ignore_errors=True)
        if clean_path.is_file():
            clean_path.unlink()

    yield str(path)

    for clean in to_clean:
        clean_path = path.joinpath(clean)
        rmtree(clean_path, ignore_errors=True)
        if clean_path.is_file():
            clean_path.unlink()
