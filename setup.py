# =====================================
# generator=datazen
# version=1.1.0
# hash=59e47f4b285f0eb3e384ba23782847b5
# =====================================

"""
vmklib - Package definition for distribution.
"""

# internal
from vmklib import PKG_NAME, VERSION, DESCRIPTION
from vmklib.setup import setup


author_info = {"name": "Vaughn Kottler",
               "email": "vaughnkottler@gmail.com",
               "username": "vkottler"}
pkg_info = {"name": PKG_NAME, "version": VERSION, "description": DESCRIPTION}
setup(
    pkg_info,
    author_info,
    entry_override="mk",
)
