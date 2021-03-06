# =====================================
# generator=datazen
# version=1.7.7
# hash=aaa4b7bc6bba37cfb6ffa976520c717f
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
