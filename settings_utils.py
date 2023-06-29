from pathlib import Path
from os import PathLike
from typing import Callable
from typing import Mapping
from typing import Union
from typing import TypeVar
from typing import TypeAlias
from collections import OrderedDict


_ReturnType = TypeVar("_ReturnType", Mapping[str, str], Path)
_P: TypeAlias = Union[int, Union[str, bytes, PathLike[str], PathLike[bytes]]]


class PathError(Exception):
    """Base error if .env path not exists."""
    pass


def _dotenv_mock() -> Callable[..., _ReturnType]:

    def _find_path(*, raise_error_if_not_found: bool = False) -> Path:
        """return founded .env path."""
        return Path(Path.cwd(), ".env")

    def _create_cfg_vls(
            *,
            dotenv_path: _P = "",
            ) -> OrderedDict[str, str]:
        """return OrderedDict with params from .env."""
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
            raise PathError(f"Path '{dotenv_path!r}' not exists.")
    _dotenv_mock.find_dotenv = _find_path  # type: ignore[attr-defined]
    _dotenv_mock.dotenv_values = _create_cfg_vls  # type: ignore[attr-defined]
    return _dotenv_mock  # type: ignore[return-value]
