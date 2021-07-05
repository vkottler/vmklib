# =====================================
# generator=datazen
# version=1.7.3
# hash=ce10f5a933e962a144ed72911e699361
# =====================================

"""
vmklib - Package definition for distribution.
"""

# third-party
from vmklib.setup import setup  # type: ignore

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
