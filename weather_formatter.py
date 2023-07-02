from abc import ABC, abstractmethod
from typing import Optional
from typing import List, ClassVar

from weather_models import FormattedWeather, WeatherDescription
from weather_models import WeatherModel, BaseWeatherIconKind
from weather_models import WeatherIcon
from weather_utils import (
        create_subscr_key,
        get_icon_by,
        UnicodeWeatherKindIcons,
        )
from colors import BasePainter, DrawMode
from base_types import ColorMapT, LiteralT, ColorableT, LiteralArg


def get_icon_by_description(
        description: WeatherDescription,
        ) -> Optional[UnicodeWeatherKindIcons]:
    """return Unicode weather icon depend on
    weather kind."""
    no_descr = ""
    icon = get_icon_by((description.main, description.description))
    if icon is None:
        icon = get_icon_by((description.main, no_descr))
    return icon


class WeatherFormatter(ABC):

    @abstractmethod
    def format_weather(self, weather: WeatherModel) -> FormattedWeather:
        pass


class OpenweatherColorFormatter(WeatherFormatter):

    _end_unicode_line: ClassVar[str] = "\u001b[0m"

    def __init__(
            self,
            painters: ColorMapT,
            mode: DrawMode,
            ) -> None:
        self._painters = painters
        self._mode = mode

    def format_weather(self, weather: WeatherModel) -> FormattedWeather:
        temperature: LiteralT = ""
        items: List[LiteralT] = []
        w_type = weather.weather_type
        w_icon = self._get_weather_icon(w_type)
        icon = self._build_icon(w_icon)
        if self._mode is DrawMode.FULLCOLOR:
            for item in (weather.temperature, icon):
                items.append(self._colorise(item))
        else:
            temperature = self._make_monochrom(weather.temperature)
            items.extend([temperature, icon.value])
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
            ) -> UnicodeWeatherKindIcons:
        icon = get_icon_by_description(description)
        return UnicodeWeatherKindIcons.EMPTY if icon is None else icon

    def _build_icon(self, icn: UnicodeWeatherKindIcons) -> BaseWeatherIconKind:
        l_arg = LiteralArg(icn.value)
        return WeatherIcon(l_arg)

    def _colorise(self, item: ColorableT) -> str:
        painter = self._get_painter_for(item)
        return painter.paint_in_color(item)

    def _make_monochrom(self, item: ColorableT) -> str:
        painter = self._get_painter_for(item)
        return painter.paint_nocolor(item)

    def _get_painter_for(self, item: ColorableT) -> BasePainter:
        key = create_subscr_key(item)
        return self._painters[key]

    def _compile(self, items: list) -> str:
        items.append(self._end_unicode_line)
        return " ".join(items)


def format_weather(weather: WeatherModel) -> str:
    """Formats weather data in string"""
    return (f"{weather.city!r}, температура {weather.temperature}°C, "
            f"{weather.weather_type}\n"
            f"Восход: {weather.sunrise.strftime('%H:%M')}\n"
            f"Закат: {weather.sunset.strftime('%H:%M')}\n")


if __name__ == "__main__":
    pass
