
""""
vmklib - Shared test utilities.
"""

# built-in
from contextlib import contextmanager
import os
import tempfile
from typing import Iterator, List

# third-party
import pkg_resources

# module under test
from vmklib import PKG_NAME


@contextmanager
def get_args() -> Iterator[List[str]]:
    """ Get command-line arguments for this testing environment. """

    tdir = tempfile.TemporaryDirectory()
    base_args = [PKG_NAME, "-C", tdir.name]
    try:
        yield base_args
    finally:
        tdir.cleanup()


def get_resource(resource_name: str) -> str:
    """ Locate the path to a test resource. """

    resource_path = os.path.join("data", resource_name)
    return pkg_resources.resource_filename(__name__, resource_path)
