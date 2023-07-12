"""
Test the 'tasks.clean' module.
"""

# third-party
from pytest import mark
from vcorelib import DEFAULT_ENCODING
from vcorelib.paths.context import tempfile

# module under test
from vmklib.tasks.clean import Clean


@mark.asyncio
async def test_clean_simple():
    """Test that we can invoke a clean task."""

    with tempfile() as tmp:
        with tmp.open("w", encoding=DEFAULT_ENCODING) as tmp_fd:
            tmp_fd.write("Hello, world!\n")
        await Clean("test").run({}, {}, tmp, tmp.with_suffix(".asdf"))
