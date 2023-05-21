from sys import stdout
from datetime import datetime
from abc import ABC, abstractmethod
from typing import NoReturn, TypeVar
from dataclasses import dataclass, asdict

from weather_models import FormattedWeather


T = TypeVar("T")


@dataclass(slots=True, frozen=True)
class DisplaySettings:
    datetime_fmt: str


class BaseWeatherPrinter(ABC):

    def __init__(self, settings: DisplaySettings) -> None:
        self._settings = settings

    @abstractmethod
    def display_weather(self, weather: FormattedWeather) -> NoReturn:
        pass


class CurrentWeatherPrinter(BaseWeatherPrinter):

    def display_weather(self, weather: FormattedWeather) -> None:
        weather_preview = self._build_preview(weather)
        self._draw(weather_preview)

    def _build_preview(self, weather: FormattedWeather) -> str:
        weather_items = asdict(weather)
        return self._create_preview(weather_items)

    def _create_preview(
            self,
            items: dict[str, str],
            ) -> dict[str, str]:
        for k, v in items.items():
            v = self._stringify_weather_item(v)
            items[k] = v
        return items

    def _stringify_weather_item(self, item: T) -> str:
        str_item = item
        if isinstance(item, datetime):
            str_item = item.strftime(self._settings.datetime_fmt)
        elif not isinstance(item, str):
            str_item = str(item)
        return str_item

    def _draw(self, preview: dict[str, str]) -> None:
        result = (
                f"{'Город / район:'.ljust(16)}{preview['city']}\n"
                f"{'Погода:'.ljust(16)}{preview['temperature']}\n"
                f"{'Описание:'.ljust(16)}{preview['weather_descr']}\n"
                f"{'Восход:'.ljust(16)}{preview['sunrise']}\n"
                f"{'Закат:'.ljust(16)}{preview['sunset']}\n"
        )
        stdout.write(result)
        stdout.flush()
