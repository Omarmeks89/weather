from sys import stdout
from datetime import datetime
from typing import TypeVar
from typing import MutableMapping as MutMapp
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict

from weather_models import FormattedWeather


ItemT = TypeVar("ItemT", contravariant=True)


@dataclass(slots=True, frozen=True)
class DisplaySettings:
    datetime_fmt: str


class BaseWeatherPrinter(ABC):
    """base class for display weather."""

    def __init__(self, settings: DisplaySettings) -> None:
        self._settings = settings

    @abstractmethod
    def display_weather(self, weather: FormattedWeather) -> None:
        pass


class CurrentWeatherPrinter(BaseWeatherPrinter):
    """class that used for display weather."""

    def display_weather(self, weather: FormattedWeather) -> None:
        weather_preview = self._build_preview(weather)
        self._draw(weather_preview)

    def _build_preview(self, weather: FormattedWeather) -> MutMapp[str, str]:
        weather_items = asdict(weather)
        return self._create_preview(weather_items)

    def _create_preview(self, items: MutMapp[str, str]) -> MutMapp[str, str]:
        for k, v in items.items():
            v = self._stringify_weather_item(v)
            items[k] = v
        return items

    def _stringify_weather_item(self, item: ItemT) -> str:
        """convert any item to str()."""
        if isinstance(item, datetime):
            return item.strftime(self._settings.datetime_fmt)
        else:
            return str(item)

    def _draw(self, preview: MutMapp[str, str]) -> None:
        result = (
                f"{'Город / район:'.ljust(16)}{preview['city']}\n"
                f"{'Погода:'.ljust(16)}{preview['temperature']}\n"
                f"{'Описание:'.ljust(16)}{preview['weather_descr']}\n"
                f"{'Восход:'.ljust(16)}{preview['sunrise']}\n"
                f"{'Закат:'.ljust(16)}{preview['sunset']}\n"
        )
        stdout.write(result)
        stdout.flush()
