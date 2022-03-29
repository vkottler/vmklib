# =====================================
# generator=datazen
# version=1.14.0
# hash=4d6c1ed02e646ac75581ebbf5850ab6d
# =====================================

"""
vmklib - Package definition for distribution.
"""

# internal
from vmklib import DESCRIPTION, PKG_NAME, VERSION

try:
    from vmklib.setup import setup
except (ImportError, ModuleNotFoundError):
    from vmklib_bootstrap.setup import setup  # type: ignore

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
        "3.6",
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
