"""
Test the 'tasks.github' module.
"""

# module under test
from vmklib.tasks.github import ensure_api_token, repo_url


def test_github_basic():
    """Test basic interactions with GitHub utilities."""

    ensure_api_token("asdf")
    ensure_api_token("asdf")
    assert (
        repo_url("test", "test")
        == "https://api.github.com/repos/test/test/releases"
    )
