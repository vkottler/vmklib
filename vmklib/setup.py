
"""
vmklib - A simpler setuptools-based package definition.
"""

# built-in
from contextlib import contextmanager
import os
import shutil
import tempfile
from typing import Dict, List, Iterator

# third-party
import setuptools  # type: ignore

REQ_DIR = "requirements"
PKG_NAME = "vmklib"


@contextmanager
def inject_self(working_dir: str) -> Iterator[None]:
    """
    If this file (and our package name) is missing from the working directory,
    copy us to our package directory.
    """

    added = False
    to_create = os.path.join(working_dir, PKG_NAME)

    try:
        if not os.path.isdir(to_create):
            os.mkdir(to_create)
            fname = os.path.join(to_create, "__init__.py")
            with open(fname, "w") as out_file:
                out_file.write(os.linesep)
            fname = os.path.join(to_create, os.path.basename(__file__))
            shutil.copyfile(__file__, fname)
            added = True
        yield
    finally:
        if added:
            shutil.rmtree(to_create)


def get_long_description(desc_filename: str = "README.md") -> str:
    """ Get a package's long-description data from a file. """

    try:
        with open(desc_filename, "r") as desc_file:
            long_description = desc_file.read()
        return long_description
    except FileNotFoundError:
        return ""


def default_requirements_file() -> str:
    """ Default location where  """

    return os.path.join(REQ_DIR, "requirements.txt")


def get_requirements(reqs_filename: str) -> List[str]:
    """ Get a package's requirements based on its requirements file. """

    try:
        with open(reqs_filename, "r") as reqs_file:
            reqs = reqs_file.read().strip().split()
        return reqs
    except FileNotFoundError:
        return []


def get_data_files(pkg_name: str, data_dir: str = "data") -> List[str]:
    """
    Get the non-code sources under a package directory's data directory.
    """

    data_files = []
    for root, _, files in os.walk(os.path.join(pkg_name, data_dir)):
        for fname in files:
            rel_name = os.path.join(root, fname).replace(pkg_name + os.sep, "")
            data_files.append(rel_name)

    return data_files


# pylint: disable=too-many-arguments
def setup(pkg_info: Dict[str, str], author_info: Dict[str, str],
          url_override: str = None, entry_override: str = None,
          console_overrides: List[str] = None,
          classifiers_override: List[str] = None) -> None:
    """
    Build a 'setuptools.setup' call with sane defaults and making assumptions
    about certain aspects of a package's structure.
    """

    if entry_override is None:
        entry_override = pkg_info["name"]

    if console_overrides is None:
        entry_str = "{}={}.entry:main".format(entry_override, pkg_info["name"])
        console_overrides = [entry_str]

    if url_override is None:
        url_fstring = "https://github.com/{}/{}"
        url_override = url_fstring.format(author_info["username"],
                                          pkg_info["name"])

    if classifiers_override is None:
        classifiers_override = [
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ]

    req_files = [default_requirements_file()]
    requirements = []
    for req_file in req_files:
        requirements += get_requirements(req_file)

    temp_dir = tempfile.TemporaryDirectory()
    working_dir = temp_dir.name
    dir_contents = os.listdir(os.getcwd())
    if pkg_info["name"] in dir_contents:
        working_dir = os.getcwd()

    with inject_self(working_dir):
        setuptools.setup(
            name=pkg_info["name"],
            version=pkg_info["version"],
            author=author_info["name"],
            author_email=author_info["email"],
            description=pkg_info["description"],
            long_description=get_long_description(),
            long_description_content_type="text/markdown",
            url=url_override,
            packages=setuptools.find_packages(),
            classifiers=classifiers_override,
            python_requires=">=3.6",
            entry_points={"console_scripts": console_overrides},
            install_requires=requirements,
            package_data={
                pkg_info["name"]: get_data_files(pkg_info["name"]),
                REQ_DIR: [os.path.basename(req) for req in req_files],
            },
        )

    temp_dir.cleanup()
