
"""
mk - A simpler setuptools-based package definition.
"""

# built-in
import os
from typing import Dict, List

# third-party
import setuptools  # type: ignore


def get_long_description(desc_filename: str = "README.md") -> str:
    """ Get a package's long-description data from a file. """

    with open(desc_filename, "r") as desc_file:
        long_description = desc_file.read()
    return long_description


def get_requirements(reqs_filename: str = None) -> List[str]:
    """ Get a package's requirements based on its requirements file. """

    # use a default file location
    if reqs_filename is None:
        reqs_filename = os.path.join("requirements", "requirements.txt")

    with open(reqs_filename, "r") as reqs_file:
        reqs = reqs_file.read().strip().split()
    return reqs


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
        install_requires=get_requirements(),
        package_data={pkg_info["name"]: get_data_files(pkg_info["name"])},
    )
