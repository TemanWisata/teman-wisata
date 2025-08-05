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

    @staticmethod
    def load_sql_file(sql_file: str | Path) -> str:
        """Load SQL file content."""
        if isinstance(sql_file, str):
            sql_file = Path(sql_file)

        if not sql_file.exists():
            msg = f"SQL file {sql_file} not found."
            raise FileNotFoundError(msg)
        with sql_file.open() as file:
            return file.read()
