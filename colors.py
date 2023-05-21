from enum import Enum
from dataclasses import dataclass, field
from typing import Protocol, NoReturn
from abc import ABC, abstractmethod
from types import MappingProxyType

from weather_utils import UnicodeWeatherKindIcons


class UnicodeColorsBaseCodes(int, Enum):
    COLD: int = 51
    ZERO: int = 15
    WARM: int = 220


class DrawMode(str, Enum):
    FULLCOLOR: str = "FULLCOLOR"
    NOCOLOR: str = "NOCOLOR"


_ICON_COLORS_MAP = {
    UnicodeWeatherKindIcons.SUNNY: 220,
    UnicodeWeatherKindIcons.CLOUDY: 251,
    UnicodeWeatherKindIcons.PARTLY_CLOUDY: 254,
    UnicodeWeatherKindIcons.RAINY: 45,
    UnicodeWeatherKindIcons.TRUNDERSTORM: 246,
    UnicodeWeatherKindIcons.SNOWY: 255,
}


@dataclass
class WeatherColor:
    color: int
    scheme: str = field(default_factory=str)

    def __post_init__(self):
        self.scheme = f"\u001b[1;38;5;{self.color}m"


class BaseTemperature(Protocol):

    @property
    def abs_value(self) -> float:
        ...


class BaseWeatherPalette(ABC):

    _palette = None

    @abstractmethod
    def set_color_by(self, temperature: BaseTemperature) -> NoReturn:
        pass


class BasePainter(ABC):

    def __init__(self, palette: BaseWeatherPalette) -> None:
        self._palette = palette

    @abstractmethod
    def paint_in_color(
            self,
            temperature: BaseTemperature,
            ) -> NoReturn:
        pass

    @abstractmethod
    def paint_nocolor(
            self,
            temperature: BaseTemperature,
            ) -> NoReturn:
        pass


def _get_icon_colors_map() -> MappingProxyType[UnicodeWeatherKindIcons, int]:
    return MappingProxyType(_ICON_COLORS_MAP)


class Unicode256WeatherPalette(BaseWeatherPalette):

    _palette = UnicodeColorsBaseCodes
    _max_color_shift = 3

    def __init__(self) -> None:
        self._shift = 6

    def set_color_by(self, temperature: BaseTemperature) -> WeatherColor:
        abs_temp_value = temperature.abs_value
        return self._mix_color(abs_temp_value)

    def _mix_color(self, value: float) -> WeatherColor:
        col_shift = int(abs(value // 10))
        if col_shift > self._max_color_shift:
            col_shift = self._max_color_shift
        color = self._fetch_color_from_palette(value, col_shift)
        return WeatherColor(color)

    def _fetch_color_from_palette(self, tempr_val: float, shift: int) -> int:
        color = None
        if tempr_val == 0:
            color = self._palette.ZERO.value
        elif tempr_val < 0:
            color = self._palette.COLD.value
        else:
            color = self._palette.WARM.value
        return color - (self._shift * shift)


class Unicode256WeatherIconsPalette(BaseWeatherPalette):

    _palette = _get_icon_colors_map()

    def set_color_by(self, icon: UnicodeWeatherKindIcons) -> WeatherColor:
        return self._mix_color(icon)

    def _mix_color(self, icon: UnicodeWeatherKindIcons) -> WeatherColor:
        color = self._fetch_color_from_palette(icon)
        return WeatherColor(color)

    def _fetch_color_from_palette(self, icon: UnicodeWeatherKindIcons) -> int:
        return self._palette.get(icon, None)


class WeatherPainter(BasePainter):

    def paint_in_color(
            self,
            temperature: BaseTemperature,
            ) -> str:
        color = self._palette.set_color_by(temperature)
        return f"{color.scheme}{temperature.draw()}"

    def paint_nocolor(
            self,
            temperature: BaseTemperature,
            ) -> str:
        return f"{temperature.draw()}"


class WeatherIconPainter(BasePainter):
    """colorised weather icons."""

    def paint_in_color(
            self,
            icon: UnicodeWeatherKindIcons,
            ) -> str:
        color = self._palette.set_color_by(icon)
        return f"{color.scheme}{icon.value}"

    def paint_nocolor(
            self,
            icon: UnicodeWeatherKindIcons,
            ) -> str:
        return f"{icon.value}"
