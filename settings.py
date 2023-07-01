import os
from sys import stderr, stdout
from collections import OrderedDict

from settings_utils import PathError


__all__ = [
        "load_config",
        ]


try:
    # dotenv haven`t stub files
    import dotenv  # type: ignore[import]
except ImportError:
    from settings_utils import _dotenv_mock
    dotenv = _dotenv_mock()


def load_config() -> OrderedDict[str, str]:
    try:
        path = _get_env_path()
        return _make_config(path)
    except PathError as err:
        msg = f"Config file .env not found. Err: {err}."
        stderr.write(f"{msg}\n")
        raise PathError(msg)


def _get_env_path() -> str:
    path = dotenv.find_dotenv(raise_error_if_not_found=True)
    if not os.path.exists(path):
        raise PathError
    return path


def _make_config(path: str) -> OrderedDict[str, str]:
    return dotenv.dotenv_values(dotenv_path=path)


if __name__ == "__main__":
    stdout.write(f"{load_config()}\n")
