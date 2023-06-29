from enum import Enum
from dataclasses import dataclass, field
from typing import Optional
from typing import TypeVar
from abc import ABC, abstractmethod

from weather_utils import UnicodeWeatherKindIcons
from weather_models import (
        BaseWeatherTemperature,
        BaseWeatherIconKind,
        )
from base_types import WeatherInfoPart, WeatherColorizer


_IconPic = TypeVar("_IconPic", str, bytes, covariant=True)
_IconNum = TypeVar("_IconNum", bound=int, covariant=True)


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


class BaseWeatherPalette(ABC):

    @abstractmethod
    def set_color_by(self, item: WeatherInfoPart) -> WeatherColor:
        pass


class BasePainter(WeatherColorizer):

    def __init__(self, palette: BaseWeatherPalette) -> None:
        self._palette = palette


def _get_icon_color(icon: _IconPic) -> Optional[_IconNum]:
    return _ICON_COLORS_MAP.get(icon, None)


class Unicode256WeatherPalette(BaseWeatherPalette):

    _max_color_shift = 3

    def __init__(self) -> None:
        self._shift = 6

    def set_color_by(self, item: BaseWeatherTemperature) -> WeatherColor:
        abs_temp_value = item.abs_value
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
            color = UnicodeColorsBaseCodes.ZERO.value
        elif tempr_val < 0:
            color = UnicodeColorsBaseCodes.COLD.value
        else:
            color = UnicodeColorsBaseCodes.WARM.value
        return color - (self._shift * shift)


class Unicode256WeatherIconPalette(BaseWeatherPalette):

    def set_color_by(self, icon: BaseWeatherIconKind) -> WeatherColor:
        return self._mix_color(icon)

    def _mix_color(self, icon: BaseWeatherIconKind) -> WeatherColor:
        color = self._fetch_color_from_palette(icon)
        return WeatherColor(color)

    def _fetch_color_from_palette(self, icon: BaseWeatherIconKind) -> int:
        return _get_icon_color(icon.picture)


class WeatherPainter(BasePainter):

    def paint_in_color(
            self,
            temperature: BaseWeatherTemperature,
            ) -> str:
        color = self._palette.set_color_by(temperature)
        return f"{color.scheme}{temperature.draw()}"

    def paint_nocolor(
            self,
            temperature: BaseWeatherTemperature,
            ) -> str:
        return f"{temperature.draw()}"


class WeatherIconPainter(BasePainter):
    """colorised weather icons."""

    def paint_in_color(
            self,
            icon: BaseWeatherIconKind,
            ) -> str:
        color = self._palette.set_color_by(icon)
        return f"{color.scheme}{icon.picture}"

    def paint_nocolor(
            self,
            icon: BaseWeatherIconKind,
            ) -> str:
        return f"{icon.picture}"
