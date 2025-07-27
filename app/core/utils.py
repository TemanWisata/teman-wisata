"""Utils for core functionality."""

from pathlib import Path

import toml


class Utils:
    """Utility class for core functionalities."""

    @staticmethod
    def get_root_path() -> Path:
        """Get the root path of the project."""
        return Path(__file__).parent.parent.parent.resolve()

    @staticmethod
    def get_version() -> str:
        """Retrieve the project version from pyproject.toml."""
        data = toml.load("pyproject.toml")
        return data["project"]["version"]
