# =====================================
# generator=datazen
# version=1.6.1
# hash=32ea9b2d7561a67edb745a95b7c6e1b3
# =====================================

"""
vmklib - Package definition for distribution.
"""

# third-party
from vmklib.setup import setup  # type: ignore

# internal
from vmklib import PKG_NAME, VERSION, DESCRIPTION


author_info = {"name": "Vaughn Kottler",
               "email": "vaughnkottler@gmail.com",
               "username": "vkottler"}
pkg_info = {"name": PKG_NAME, "version": VERSION, "description": DESCRIPTION}
setup(
    pkg_info,
    author_info,
    entry_override="mk",
)
