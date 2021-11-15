# =====================================
# generator=datazen
# version=1.9.0
# hash=1b779f83ea09cc421cd4bc0c7ace4b21
# =====================================

"""
vmklib - Package definition for distribution.
"""

# third-party
from vmklib.setup import setup

# internal
from vmklib import PKG_NAME, VERSION, DESCRIPTION


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
    ],
}
setup(
    pkg_info,
    author_info,
    entry_override="mk",
)
