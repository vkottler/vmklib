"""
An interface exposing miscellaneous utilities.
"""


def to_slug(data: str) -> str:
    """Convert a string to an import slug."""
    return data.replace("-", "_")
