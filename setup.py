# =====================================
# generator=datazen
# version=1.14.0
# hash=77111c33324b64990fdbd486c8b83e31
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
    entry_points={"console_scripts": ["mk=vmklib.entry:main"]},
)
