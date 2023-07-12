"""
Test the 'tasks.mixins.curl' module.
"""

# third-party
from pytest import mark

# module under test
from vmklib.tasks.mixins.curl import CurlMixin


@mark.asyncio
async def test_curl_simple():
    """Test that we can invoke curl methods."""

    test = CurlMixin("help")
    await test.curl("--help", post_data={"a": 1}, headers={"Test": "123"})
