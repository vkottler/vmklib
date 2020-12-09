
"""
datazen - Test the program's entry-point.
"""

# built-in
import os
import tempfile

# third-party
import pkg_resources

# module under test
from vmklib import PKG_NAME
from vmklib.entry import main as mk_main


def get_resource(resource_name: str) -> str:
    """ Locate the path to a test resource. """

    resource_path = os.path.join("data", resource_name)
    return pkg_resources.resource_filename(__name__, resource_path)


def test_entry():
    """ Test some basic command-line argument scenarios. """

    tdir = tempfile.TemporaryDirectory()

    base_args = [PKG_NAME, "-C", tdir.name]
    good_base_args = base_args + ["-f", get_resource("Makefile")]

    assert mk_main(good_base_args + ["test"]) == 0
    assert mk_main(good_base_args + ["--proj", "test", "test"]) == 0
    assert mk_main(good_base_args + ["-p", "prefix", "test"]) == 0
    assert mk_main(good_base_args + ["test_bad"]) != 0
    assert mk_main(good_base_args + ["--weird-option", "yo"]) != 0
    assert mk_main(base_args + ["-f", "nah"]) != 0

    tdir.cleanup()
