"""Test for the project_version module."""

from app.core.utils import Utils


def test_get_version() -> None:
    """Test the get_version function from project_version module."""
    version = Utils.get_version()
    number_of_dots_in_version = 2
    assert isinstance(version, str), "Version should be a string"
    assert version, "Version should not be empty"
    assert version.count(".") == number_of_dots_in_version, "Version format should be 'major.minor.patch'"
