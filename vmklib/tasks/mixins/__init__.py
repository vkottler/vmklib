"""
A module for aggregating mixin classes.
"""

# internal
from vmklib.tasks.mixins.concrete import (
    ConcreteBuilderMixin,
    ConcreteOnceMixin,
)
from vmklib.tasks.mixins.curl import CommandResult, CurlMixin, curl_headers

__all__ = [
    "ConcreteBuilderMixin",
    "ConcreteOnceMixin",
    "CurlMixin",
    "curl_headers",
    "CommandResult",
]
