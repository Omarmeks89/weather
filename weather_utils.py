from enum import Enum
from typing import MutableMapping, Mapping
from typing import Optional
from typing import Sequence, TypeAlias
from typing import Union

from base_types import WeatherInfoPart, WeatherColorizer


_Literal: TypeAlias = Union[str, bytes]


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


_OPW_WEATHER_ICONS_MAP: Mapping[Sequence[str], str] = {
    _OPW_KindCodes.THUNDERSTORM.value: UnicodeWeatherKindIcons.TRUNDERSTORM,
    _OPW_KindCodes.DRIZZLE.value: UnicodeWeatherKindIcons.RAINY,
    _OPW_KindCodes.RAIN.value: UnicodeWeatherKindIcons.RAINY,
    _OPW_KindCodes.SNOW.value: UnicodeWeatherKindIcons.SNOWY,
    _OPW_KindCodes.CLEAR.value: UnicodeWeatherKindIcons.SUNNY,
    _OPW_KindCodes.PARTLY_CLOUDS: UnicodeWeatherKindIcons.PARTLY_CLOUDY,
    _OPW_KindCodes.CLOUDS: UnicodeWeatherKindIcons.CLOUDY,
}


def get_icons_map(icon_key: Sequence[str]) -> Optional[str]:
    """TODO rename - get_icon_by_key(...)."""
    try:
        return _OPW_WEATHER_ICONS_MAP[icon_key]
    except KeyError:
        return None


def subscribe_coloriser(
        key_type: WeatherInfoPart,
        coloriser: WeatherColorizer,
        collection: MutableMapping[_Literal, WeatherColorizer],
        ) -> None:
    """subscribe painters on weatheritem class name."""
    key = create_subscr_key(key_type)
    if key not in collection:
        collection[key] = coloriser


def create_subscr_key(item: WeatherInfoPart) -> _Literal:
    """make str from item name for using as key in coll."""
    if isinstance(item, type):
        return item.__name__
    return type(item).__name__
