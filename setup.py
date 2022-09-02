# =====================================
# generator=datazen
# version=3.0.10
# hash=f204f536c4a3d076509f29c80019b3ce
# =====================================

"""
vmklib - Package definition for distribution.
"""

# third-party
try:
    from setuptools_wrapper.setup import setup
except (ImportError, ModuleNotFoundError):
    from vmklib_bootstrap.setup import setup  # type: ignore

# internal
from vmklib import DESCRIPTION, PKG_NAME, VERSION

author_info = {
    "name": "Vaughn Kottler",
    "email": "vaughnkottler@gmail.com",
    "username": "vkottler",
}
pkg_info = {
    "name": PKG_NAME,
    "slug": PKG_NAME.replace("-", "_"),
    "version": VERSION,
    "description": DESCRIPTION,
    "versions": [
        "3.7",
        "3.8",
        "3.9",
        "3.10",
    ],
}
setup(
    pkg_info,
    author_info,
)
