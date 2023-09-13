# =====================================
# generator=datazen
# version=3.1.2
# hash=b10cdc2e4759a797bc0d36b525de6ade
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
        "3.10",
        "3.11",
    ],
}
setup(
    pkg_info,
    author_info,
)
