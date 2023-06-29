from abc import ABC, abstractmethod
from typing import Optional
from typing import TypeVar

from weather_models import FormattedWeather, WeatherDescription
from weather_models import Weather, WeatherModel
from weather_utils import (
        create_subscr_key,
        get_icons_map,
        UnicodeWeatherKindIcons,
        WeatherInfoPart,
        )
from colors import BasePainter, DrawMode


T = TypeVar("T", bound=WeatherInfoPart, covariant=True)


def get_icon_by_description(
        description: WeatherDescription,
        ) -> Optional[UnicodeWeatherKindIcons]:
    """return Unicode weather icon depend on
    weather kind."""
    no_descr = ""
    icon = get_icons_map((description.main, description.description))
    if icon is None:
        icon = get_icons_map((description.main, no_descr))
    return icon


class WeatherFormatter(ABC):

    @abstractmethod
    def format_weather(self, weather: Weather) -> FormattedWeather:
        pass


class OpenweatherColorFormatter(WeatherFormatter):

    _end_unicode_line: str = "\u001b[0m"

    def __init__(
            self,
            painters: dict[str, BasePainter],
            mode: DrawMode,
            ) -> None:
        self._painters = painters
        self._mode = mode

    def format_weather(self, weather: WeatherModel) -> FormattedWeather:
        temperature = None
        items = []
        w_type = weather.weather_type
        w_icon = self._get_weather_icon(w_type)
        # have to format icon to concrete system type.
        if self._mode is DrawMode.FULLCOLOR:
            for item in (weather.temperature, w_icon):
                items.append(self._colorise(item))
        else:
            temperature = self._make_monochrom(weather.temperature)
            items.extend([temperature, w_icon])
        full_weather_str = self._compile(items)
        items.clear()
        return FormattedWeather(
                city=weather.city,
                temperature=full_weather_str,
                weather_descr=w_type.description,
                sunrise=weather.sunrise,
                sunset=weather.sunset,
        )

    def _get_weather_icon(
            self,
            description: WeatherDescription,
            ) -> Optional[UnicodeWeatherKindIcons]:
        icon = get_icon_by_description(description)
        return "" if icon is None else icon

    def _colorise(self, item: T) -> str:
        painter = self._get_painter_for(item)
        return painter.paint_in_color(item)

    def _make_monochrom(self, item: T) -> str:
        painter = self._get_painter_for(item)
        return painter.paint_nocolor(item)

    def _get_painter_for(self, item: T) -> BasePainter:
        key = create_subscr_key(item)
        return self._painters.get(key)

    def _compile(self, items: list) -> str:
        items.append(self._end_unicode_line)
        return " ".join(items)


def format_weather(weather: Weather) -> str:
    """Formats weather data in string"""
    return (f"{weather.city}, температура {weather.temperature}°C, "
            f"{weather.weather_type}\n"
            f"Восход: {weather.sunrise.strftime('%H:%M')}\n"
            f"Закат: {weather.sunset.strftime('%H:%M')}\n")


if __name__ == "__main__":
    from datetime import datetime
    from weather_api_service import WeatherType
    print(format_weather(Weather(
        temperature=25,
        weather_type=WeatherType.CLEAR,
        sunrise=datetime.fromisoformat("2022-05-03 04:00:00"),
        sunset=datetime.fromisoformat("2022-05-03 20:25:00"),
        city="Moscow"
    )))
