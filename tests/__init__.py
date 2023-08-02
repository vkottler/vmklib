""""
vmklib - Shared test utilities.
"""

# built-in
from contextlib import contextmanager
import os
from shutil import rmtree
import tempfile
from typing import Iterator, List

# third-party
import pkg_resources

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

    resource_path = os.path.join("data", resource_name)
    return pkg_resources.resource_filename(__name__, resource_path)


@contextmanager
def build_cleaned_resource(resource_name: str) -> Iterator[str]:
    """
    Get a path to a resourc and ensure that a 'build' directory relative to it
    is cleaned up before and after providing it.
    """

    path = get_resource(resource_name)

    # Try our best to clean up virtual environments.
    to_clean = ["build", "venv"] + [
        f"venv3.{x}" for x in [6, 7, 8, 9, 10, 11, 12]
    ]

    for clean in to_clean:
        clean_path = os.path.join(path, clean)
        rmtree(clean_path, ignore_errors=True)

    yield path

    for clean in to_clean:
        clean_path = os.path.join(path, clean)
        rmtree(clean_path, ignore_errors=True)
