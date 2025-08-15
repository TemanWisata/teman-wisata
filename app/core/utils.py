"""Utils for core functionality."""

from pathlib import Path

import toml
from loguru import logger


class Utils:
    """Utility class for core functionalities."""

    @classmethod
    def get_root_path(cls) -> Path:
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

    @classmethod
    def get_static_path(cls) -> Path:
        """Get the static files path."""
        static_path = cls.get_root_path().joinpath("ui", "dist")
        if not static_path.exists():
            msg = f"Static path {static_path} does not exist."
            logger.error(msg)
            raise FileNotFoundError(msg)
        if not static_path.is_dir():
            msg = f"Static path {static_path} is not a directory."
            logger.error(msg)
            raise NotADirectoryError(msg)
        return static_path
