from dataclasses import dataclass
from datetime import datetime
from typing import TypeAlias, NoReturn
from abc import ABC, abstractmethod
from enum import Enum


Celsius: TypeAlias = float
WeatherType: TypeAlias = str
TemperatureValue: TypeAlias = float


__all__ = [
        "CelsiusTemperature",
        "FarenheitTemperature",
        "BaseTemperature",
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


class BaseTemperature(ABC):

    _scale = _TempScaleUnicodeSymbols

    def __init__(self, temp: TemperatureValue) -> None:
        self._temp = temp

    def __repr__(self) -> str:
        return f"{type(self).__name__} {self._temp}{self._temp_kind}"

    @property
    def kind(self) -> str:
        return self._temp_kind

    @property
    @abstractmethod
    def abs_value(self) -> NoReturn:
        """abs value celsius."""
        pass

    def draw(self) -> str:
        return f"{self._temp}{self._temp_kind}"


class CelsiusTemperature(BaseTemperature):

    def __init__(self, temp: TemperatureValue) -> None:
        super().__init__(temp)
        self._temp_kind = self._scale.CELSIUS

    @property
    def abs_value(self) -> TemperatureValue:
        return self._temp


class FarenheitTemperature(BaseTemperature):

    def __init__(self, temp: TemperatureValue) -> None:
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
    temperature: BaseTemperature
    weather_type: WeatherDescription
    sunrise: datetime
    sunset: datetime
    city: str
