# =====================================
# generator=datazen
# version=1.9.0
# hash=091f7871148ddd40eef4ad38027e0162
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
    ],
}
setup(
    pkg_info,
    author_info,
    entry_override="mk",
)
