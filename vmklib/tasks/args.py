"""
A module for assisting with getting optional arguments for tasks.
"""

# built-in
from os import environ
from typing import Any, List


def environ_fallback(key: str, _default: Any = None, **kwargs) -> Any:
    """
    Attempt to retrieve a value from keyword arguments, otherwise also fall
    back to system environment variables.
    """
    return {**kwargs}.get(key, environ.get(key, _default))


def environ_fallback_split(key: str, **kwargs) -> List[str]:
    """
    Get whitespace-separated arguments from the environment or keyword
    arguments.
    """
    return [str(x) for x in environ_fallback(key, "", **kwargs).split()]
