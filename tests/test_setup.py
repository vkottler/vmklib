
"""
datazen - Test the 'setup' module.
"""

# third-party
import os
import tempfile
import setuptools  # type: ignore

# module under test
from vmklib import PKG_NAME, VERSION, DESCRIPTION
from vmklib.setup import setup as setup_fn


def test_setup_fn():
    """
    Test that that package-building capability we expose externally works.
    """

    author_info = {"name": "Vaughn Kottler",
                   "email": "vaughnkottler@gmail.com",
                   "username": "vkottler"}
    pkg_info = {"name": PKG_NAME,
                "version": VERSION,
                "description": DESCRIPTION}

    def setup_stub(*_, **__):
        """ Don't do anything. """

    real_setup = setuptools.setup
    setuptools.setup = setup_stub

    start_dir = os.getcwd()

    with tempfile.TemporaryDirectory() as temp_dir:
        setup_fn(pkg_info, author_info, entry_override="mk")
        setup_fn(pkg_info, author_info)
        os.chdir(temp_dir)
        setup_fn(pkg_info, author_info)
        os.chdir(start_dir)

    setuptools.setup = real_setup
