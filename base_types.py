from abc import ABC, abstractmethod
from typing import TypeVar
from typing import Generic
from typing_extensions import Self
from typing import Union, cast


_T = TypeVar("_T", contravariant=True)
_TC = TypeVar("_TC", covariant=True)


class WeatherArg(Generic[_T, _TC]):
    """Base generic type."""

    def __init__(self, value: _T) -> None:
        self._value = value

    @property
    def value(self) -> _TC:
        """cast _T to covariant type."""
        return cast(_TC, self._value)


class NumericArg(WeatherArg):
    """represents types like int and float."""

    def __init__(self, value: Union[int, float]) -> None:
        self._value = value

    def __repr__(self) -> str:
        return f"{type(self).__name__}(value={self._value})"

    @property
    def value(self) -> Union[int, float]:
        return self._value


class LiteralArg(WeatherArg):
    """Represents types like str | bytes."""

    def __init__(self, value: Union[str, bytes]) -> None:
        self._value = value

    def __repr__(self) -> str:
        return f"{type(self).__name__}(value={self._value})"

    @property
    def value(self) -> Union[str, bytes]:
        return self._value


class WeatherInfoPart(ABC):
    """class represents any isinstance
    of weather."""

    @classmethod
    @abstractmethod
    def rebuild(cls, item: WeatherArg) -> Self:
        """factory method for runtime rebuilding."""
        pass

    @abstractmethod
    def draw(self) -> str:
        """draw value as string."""
        pass


class WeatherColorizer(ABC):

    @abstractmethod
    def paint_in_color(self, item: WeatherInfoPart) -> str: pass

    @abstractmethod
    def paint_no_color(self, item: WeatherInfoPart) -> str: pass
