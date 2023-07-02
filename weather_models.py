from dataclasses import dataclass
from datetime import datetime
from typing import TypeAlias, TypeVar, Type, cast
from enum import Enum

from base_types import WeatherArg, WeatherInfoPart, LiteralT, NumericT


WeatherType: TypeAlias = str

TemperatureT = TypeVar(
        "TemperatureT",
        bound="BaseWeatherTemperature",
        covariant=True,
        )
IconT = TypeVar(
        "IconT",
        bound="BaseWeatherIconKind",
        covariant=True,
        )


__all__ = [
        "CelsiusTemperature",
        "FarenheitTemperature",
        "BaseWeatherTemperature",
        "WeatherModel",
        "FormattedWeather",
        "WeatherDescription",
        ]


class _TempScaleUnicodeSymbols(str, Enum):
    """Unicode symbols numbres."""
    CELSIUS: str = "\u2103"
    FARENHEIT: str = "\u2109"


class BaseWeatherTemperature(WeatherInfoPart):
    """Base class, represents temperature object."""

    _scale = _TempScaleUnicodeSymbols

    def __init__(self, value: WeatherArg) -> None:
        """TODO do we type check or assert here?"""
        self._temp = value
        self._temp_kind = ""

    @classmethod
    def rebuild(cls: Type[TemperatureT], item: WeatherArg) -> TemperatureT:
        return cast(TemperatureT, cls(item))

    def __repr__(self) -> str:
        return f"{type(self).__name__} {self._temp.value}{self._temp_kind}"

    @property
    def kind(self) -> str:
        return self._temp_kind

    def draw(self) -> str:
        tmpr_value = self._temp.value
        return f"{tmpr_value}{self._temp_kind}"


class BaseWeatherIconKind(WeatherInfoPart):
    """Base class, represents Unicode icon object."""

    def __init__(self, value: WeatherArg) -> None:
        self._value = value

    @classmethod
    def rebuild(cls: Type[IconT], item: WeatherArg) -> IconT:
        return cast(IconT, cls(item))

    @property
    def value(self) -> LiteralT:
        return self._value.value

    def draw(self) -> str:
        ic_value = self._value.value
        return str(ic_value)


class WeatherIcon(BaseWeatherIconKind):
    """Simple base icon."""

    def __init__(self, value: WeatherArg) -> None:
        super().__init__(value)

    def __repr__(self) -> str:
        return self.draw()


class CelsiusTemperature(BaseWeatherTemperature):

    def __init__(self, temp: WeatherArg) -> None:
        super().__init__(temp)
        self._temp_kind = self._scale.CELSIUS

    @property
    def value(self) -> NumericT:
        return self._temp.value


class FarenheitTemperature(BaseWeatherTemperature):

    def __init__(self, temp: WeatherArg) -> None:
        super().__init__(temp)
        self._temp_kind = self._scale.FARENHEIT

    @property
    def value(self) -> NumericT:
        return (self._temp.value - 32) * (5 / 9)


@dataclass(slots=True)
class WeatherDescription:
    main: str
    description: str


@dataclass
class FormattedWeather:
    city: LiteralT
    temperature: str
    weather_descr: str
    sunrise: datetime
    sunset: datetime


@dataclass
class WeatherModel:
    temperature: BaseWeatherTemperature
    weather_type: WeatherDescription
    sunrise: datetime
    sunset: datetime
    city: LiteralT
