"""Module to get the project version from pyproject.toml."""

import toml


def get_version() -> str:
    """Retrieve the project version from pyproject.toml."""
    data = toml.load("pyproject.toml")
    return data["project"]["version"]
