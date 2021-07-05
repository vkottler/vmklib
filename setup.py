# =====================================
# generator=datazen
# version=1.7.4
# hash=75bc4128b0ba5edd0ee960cac6d2a8c1
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
pkg_info = {"name": PKG_NAME, "version": VERSION, "description": DESCRIPTION}
setup(
    pkg_info,
    author_info,
    entry_override="mk",
)
