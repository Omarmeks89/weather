from enum import Enum
from typing import Mapping
from typing import Optional
from typing import Sequence

from base_types import LiteralT, ColorMapT, WeatherColorizer, _T


class TemperatureScaleKind(str, Enum):
    CELSIUS: str = "celsius"
    FARENHEIT: str = "farenheit"


class _OPW_KindCodes(tuple, Enum):
    THUNDERSTORM: tuple = ("Thunderstorm", "", )
    DRIZZLE: tuple = ("Drizzle", "", )
    RAIN: tuple = ("Rain", "", )
    SNOW: tuple = ("Snow", "", )
    CLEAR: tuple = ("Clear", "", )
    PARTLY_CLOUDS: tuple = ("Clouds", "few clouds", )
    CLOUDS: tuple = ("Clouds", "", )


class UnicodeWeatherKindIcons(str, Enum):
    """unicode icons for weather kind."""
    SUNNY: str = "\U0001f31e"
    PARTLY_CLOUDY: str = "\U0001f324"
    CLOUDY: str = "\U0001f325"
    RAINY: str = "\U0001f327"
    TRUNDERSTORM: str = "\u26c8"
    SNOWY: str = "\u2744"
    EMPTY: str = ""


_OPW_WEATHER_ICONS: Mapping[Sequence[LiteralT], UnicodeWeatherKindIcons] = {
    _OPW_KindCodes.THUNDERSTORM.value: UnicodeWeatherKindIcons.TRUNDERSTORM,
    _OPW_KindCodes.DRIZZLE.value: UnicodeWeatherKindIcons.RAINY,
    _OPW_KindCodes.RAIN.value: UnicodeWeatherKindIcons.RAINY,
    _OPW_KindCodes.SNOW.value: UnicodeWeatherKindIcons.SNOWY,
    _OPW_KindCodes.CLEAR.value: UnicodeWeatherKindIcons.SUNNY,
    _OPW_KindCodes.PARTLY_CLOUDS: UnicodeWeatherKindIcons.PARTLY_CLOUDY,
    _OPW_KindCodes.CLOUDS: UnicodeWeatherKindIcons.CLOUDY,
}


def get_icons_map(ic_key: Sequence[str]) -> Optional[UnicodeWeatherKindIcons]:
    """TODO rename - get_icon_by_key(...)."""
    return _OPW_WEATHER_ICONS.get(ic_key, None)


def subscribe_coloriser(
        key_type: _T,
        coloriser: WeatherColorizer,
        collection: ColorMapT,
        ) -> None:
    """subscribe painters on weatheritem class name."""
    key = create_subscr_key(key_type)
    if key not in collection:
        collection[key] = coloriser


def create_subscr_key(item: _T) -> LiteralT:
    """make str from item name for using as key in coll."""
    if isinstance(item, type):
        return item.__name__
    return type(item).__name__
