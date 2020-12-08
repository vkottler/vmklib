# =====================================
# generator=datazen
# version=1.0.11
# hash=977feda7e8780285af82d15af66597c5
# =====================================

"""
mk - Package definition for distribution.
"""

# internal
from mk import PKG_NAME, VERSION, DESCRIPTION
from mk.setup import setup


author_info = {"name": "Vaughn Kottler",
               "email": "vaughnkottler@gmail.com",
               "username": "vkottler"}
pkg_info = {"name": PKG_NAME, "version": VERSION, "description": DESCRIPTION}
setup(
    pkg_info,
    author_info,
)
