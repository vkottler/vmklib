# =====================================
# generator=datazen
# version=1.2.1
# hash=bb263e50cd25b96694770405cd647e56
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
