from pathlib import Path
from typing import Callable, Optional
from collections import OrderedDict


class PathError(Exception):
    """Base error if .env path not exists."""
    pass


def _dotenv_mock() -> Callable:

    def _find_path(*, raise_error_if_not_found: bool = False) -> str:
        return Path(Path.cwd(), ".env")

    def _create_config_values(
            *,
            dotenv_path: Optional[str] = None,
            ) -> OrderedDict[str, str]:
        config = OrderedDict()
        try:
            with open(dotenv_path, "r") as fd:
                for line in fd.readlines():
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    key, value = line.split("=", 1)
                    config[key] = value
            return config
        except FileNotFoundError:
            raise PathError(f"Path '{dotenv_path}' not exists.")

    _dotenv_mock.find_dotenv = _find_path
    _dotenv_mock.dotenv_values = _create_config_values
    return _dotenv_mock
