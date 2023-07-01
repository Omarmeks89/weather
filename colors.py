from enum import Enum
from dataclasses import dataclass, field
from typing import Optional
from typing import TypeAlias
from abc import ABC, abstractmethod
from typing import Mapping

from weather_utils import UnicodeWeatherKindIcons
from base_types import WeatherInfoPart, WeatherColorizer, LiteralT


ColorableT: TypeAlias = WeatherInfoPart


class UnicodeColorsBaseCodes(int, Enum):
    COLD: int = 51
    ZERO: int = 15
    WARM: int = 220


class DrawMode(str, Enum):
    FULLCOLOR: str = "FULLCOLOR"
    NOCOLOR: str = "NOCOLOR"


_ICON_COLORS_MAP: Mapping[LiteralT, int] = {
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
    def set_color_by(self, item: ColorableT) -> WeatherColor:
        pass


class BasePainter(WeatherColorizer):

    def __init__(self, palette: BaseWeatherPalette) -> None:
        self._palette = palette


def _get_icon_color(icon: LiteralT) -> Optional[int]:
    return _ICON_COLORS_MAP.get(icon, None)


class Unicode256WeatherPalette(BaseWeatherPalette):

    _max_color_shift = 3

    def __init__(self) -> None:
        self._shift = 6

    def set_color_by(self, item: ColorableT) -> WeatherColor:
        abs_temp_value = item.value
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

    def set_color_by(self, icon: ColorableT) -> WeatherColor:
        return self._mix_color(icon)

    def _mix_color(self, icon: ColorableT) -> WeatherColor:
        color = self._fetch_clr_from_palette(icon)
        if color is None:
            raise Exception
        return WeatherColor(color)

    def _fetch_clr_from_palette(self, icon: ColorableT) -> Optional[int]:
        return _get_icon_color(icon.value)


class WeatherPainter(BasePainter):

    def paint_in_color(
            self,
            temperature: WeatherInfoPart,
            ) -> str:
        color = self._palette.set_color_by(temperature)
        return f"{color.scheme}{temperature.draw()}"

    def paint_nocolor(
            self,
            temperature: WeatherInfoPart,
            ) -> str:
        return f"{temperature.draw()}"


class WeatherIconPainter(BasePainter):
    """colorised weather icons."""

    def paint_in_color(
            self,
            icon: WeatherInfoPart,
            ) -> str:
        color = self._palette.set_color_by(icon)
        return f"{color.scheme}{icon.draw()}"

    def paint_nocolor(
            self,
            icon: WeatherInfoPart,
            ) -> str:
        return f"{icon.draw()}"
