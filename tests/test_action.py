"""Unit tests for Action."""

from bond_api import Action


def test_action_eq():
    """Tests that different Action instances compare correctly."""
    assert Action("name-1", argument="arg-1") == Action("name-1", argument="arg-1")
    assert Action("name-1", argument="arg-1") != Action("name-other", argument="arg-1")
    assert Action("name-1", argument="arg-1") != Action("name-1", argument="arg-other")
    assert Action("name-1", argument="arg-1") != Action("name-other", argument="arg-other")
