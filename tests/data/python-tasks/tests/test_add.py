"""
A module for testing the 'add' function.
"""

# module under test
from python_tasks import add


def test_add():
    """Test the 'add' function."""
    assert add(1, 1) == 2
