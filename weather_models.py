from dataclasses import dataclass
from typing_extensions import Self
from datetime import datetime
from typing import TypeAlias, Union
from abc import ABC, abstractmethod
from enum import Enum

from base_types import WeatherArg, WeatherInfoPart


Celsius: TypeAlias = float
WeatherType: TypeAlias = str
TemperatureValue: TypeAlias = Union[int, float]


__all__ = [
        "CelsiusTemperature",
        "FarenheitTemperature",
        "BaseWeatherTemperature",
        "Weather",
        "WeatherModel",
        "FormattedWeather",
        "WeatherDescription",
        "Celsius",
        ]


class _TempScaleUnicodeSymbols(str, Enum):
    """Unicode symbols numbres."""
    CELSIUS: str = "\u2103"
    FARENHEIT: str = "\u2109"


class _AbsTemperatureMixin(ABC):
    """Mixin that repr-ts add temperature interface."""

    @property
    @abstractmethod
    def abs_value(self) -> TemperatureValue:
        pass


class BaseWeatherTemperature(_AbsTemperatureMixin, WeatherInfoPart):
    """Base class, represents temperature object."""

    _scale = _TempScaleUnicodeSymbols

    def __init__(self, value: WeatherArg) -> None:
        """TODO do we type check or assert here?"""
        self._temp = value.value
        self._temp_kind = ""

    @classmethod
    def rebuild(cls, item: WeatherArg) -> Self:
        return cls(item)

    def __repr__(self) -> str:
        return f"{type(self).__name__} {self._temp}{self._temp_kind}"

    @property
    def kind(self) -> str:
        return self._temp_kind

    def draw(self) -> str:
        return f"{self._temp}{self._temp_kind}"


class BaseWeatherIconKind(WeatherInfoPart):
    """Base class, represents Unicode icon object."""

    def __init__(self, value: WeatherArg) -> None:
        self._value = value

    @classmethod
    @abstractmethod
    def rebuild(cls, item: WeatherArg) -> Self: pass

    def draw(self) -> str:
        return str(self._value)


class CelsiusTemperature(BaseWeatherTemperature):

    def __init__(self, temp: WeatherArg) -> None:
        super().__init__(temp)
        self._temp_kind = self._scale.CELSIUS

    @property
    def abs_value(self) -> TemperatureValue:
        return self._temp


class FarenheitTemperature(BaseWeatherTemperature):

    def __init__(self, temp: WeatherArg) -> None:
        super().__init__(temp)
        self._temp_kind = self._scale.FARENHEIT

    @property
    def abs_value(self) -> TemperatureValue:
        return (self._temp - 32) * (5 / 9)


@dataclass(slots=True)
class WeatherDescription:
    main: str
    description: str


@dataclass
class FormattedWeather:
    city: str
    temperature: str
    weather_descr: str
    sunrise: datetime
    sunset: datetime


@dataclass(slots=True, frozen=True)
class Weather:
    temperature: Celsius
    weather_type: WeatherType
    sunrise: datetime
    sunset: datetime
    city: str


@dataclass
class WeatherModel:
    temperature: BaseWeatherTemperature
    weather_type: WeatherDescription
    sunrise: datetime
    sunset: datetime
    city: str
