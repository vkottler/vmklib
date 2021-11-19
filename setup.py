# =====================================
# generator=datazen
# version=1.9.0
# hash=76b4488474014107d8c26255f2c388e6
# =====================================

"""
vmklib - Package definition for distribution.
"""

# internal
from vmklib import DESCRIPTION, PKG_NAME, VERSION

try:
    from vmklib.setup import setup
except ImportError:
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
