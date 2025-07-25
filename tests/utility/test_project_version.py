"""Test for the project_version module."""

from app.utils import get_version


def test_get_version() -> None:
    """Test the get_version function from project_version module."""
    version = get_version()
    number_of_dots_in_version = 2
    assert isinstance(version, str), "Version should be a string"  # noqa: S101
    assert version, "Version should not be empty"  # noqa: S101
    assert version.count(".") == number_of_dots_in_version, "Version format should be 'major.minor.patch'"  # noqa: S101
