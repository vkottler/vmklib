"""
vmklib - A simpler setuptools-based package definition.
"""

# built-in
from contextlib import contextmanager
import os
import shutil
import tempfile
from typing import Any, Dict, List, Iterator

# third-party
import setuptools  # type: ignore

REQ_DIR = "requirements"
PKG_NAME = "vmklib"


@contextmanager
def inject_self(working_dir: str) -> Iterator[None]:
    """
    Copy this entire package into the caller's source distribution. This is
    the only way to avoid a pointless requirement to already have this package
    installed to install anything else, and also generally not requiring
    an explicit install of this package except for command-line use.
    """

    added = False
    to_create = os.path.join(working_dir, PKG_NAME)

    try:
        if not os.path.isdir(to_create):
            os.mkdir(to_create)

            # copy our sources into their package
            to_copy = ["__init__.py", "app.py", "entry.py", "setup.py"]
            vmklib_dir = os.path.dirname(__file__)
            for fname in to_copy:
                dest = os.path.join(to_create, fname)
                if not os.path.isfile(dest):
                    shutil.copyfile(os.path.join(vmklib_dir, fname), dest)

            added = True
        yield
    finally:
        if added:
            shutil.rmtree(to_create)


def get_long_description(desc_filename: str = "README.md") -> str:
    """Get a package's long-description data from a file."""

    try:
        with open(desc_filename, "r") as desc_file:
            long_description = desc_file.read()
        return long_description
    except FileNotFoundError:
        return ""


def default_requirements_file() -> str:
    """Default location where"""

    return os.path.join(REQ_DIR, "requirements.txt")


def get_requirements(reqs_filename: str) -> List[str]:
    """Get a package's requirements based on its requirements file."""

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
def setup(
    pkg_info: Dict[str, Any],
    author_info: Dict[str, str],
    url_override: str = None,
    entry_override: str = None,
    console_overrides: List[str] = None,
    classifiers_override: List[str] = None,
) -> None:
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
        url_override = url_fstring.format(
            author_info["username"], pkg_info["name"]
        )

    if classifiers_override is None:
        classifiers_override = [
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ]
    for version in pkg_info.get("versions", []):
        classifiers_override.append(
            "Programming Language :: Python :: {}".format(version)
        )

    req_files = [default_requirements_file()]
    requirements = []
    for req_file in req_files:
        requirements += get_requirements(req_file)

    with tempfile.TemporaryDirectory() as temp_dir:
        working_dir = temp_dir
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
                packages=setuptools.find_packages(
                    exclude=["tests", "tests.*"]
                ),
                classifiers=classifiers_override,
                python_requires=">={}".format(
                    pkg_info.get("versions", ["3.6"])[0]
                ),
                entry_points={"console_scripts": console_overrides},
                install_requires=requirements,
                package_data={
                    pkg_info["name"]: (
                        get_data_files(pkg_info["name"])
                        + ["py.typed", "*.pyi"]
                    ),
                    "": ["*.pyi"],
                    REQ_DIR: [os.path.basename(req) for req in req_files],
                },
            )
