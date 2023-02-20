"""
Test the 'tasks.node' module.
"""

# third-party
from pytest import mark

# module under test
from vmklib.tasks.node import Npx


@mark.asyncio
async def test_npx_simple():
    """Test that we can invoke an npx task."""

    await Npx("help").run({}, {}, "--help")
