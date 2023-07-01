from typing import Literal, Union, TypeAlias, cast

from settings import load_config
from weather_utils import (
        subscribe_coloriser,
)
from colors import (
        Unicode256WeatherPalette,
        Unicode256WeatherIconPalette,
        WeatherPainter,
        WeatherIconPainter,
        DrawMode,
)
from weather_models import (
        CelsiusTemperature,
        FarenheitTemperature,
        WeatherIcon,
)
from weather_formatter import OpenweatherColorFormatter
from weather_api_service import OPW_WeatherService
from view import DisplaySettings, CurrentWeatherPrinter
from base_types import ColorMapT


DimUnit: TypeAlias = Union[Literal["metric"], Literal["imperial"]]


__all__ = [
        "formatter",
        "weather_service",
        "weather_printer",
        ]


app_config = load_config()

COLORISERS: ColorMapT = {}
USE_ROUNDED_COORDS = False
UNITS: DimUnit = cast(DimUnit, app_config["OPW_DEF_UNITS"])
OPENWEATHER_API = app_config["OPW_APIKEY"]
DEF_DATETIME_FMT = app_config["DATETIME_FMT"]
LANG = app_config["OPW_DEF_LANG"]
OPENWEATHER_URL = (
    "https://api.openweathermap.org/data/2.5/weather?"
    "lat={latitude}&lon={longitude}&"
    "appid="
    f"{OPENWEATHER_API}"
    f"&lang={LANG}&"
    f"units={UNITS}"
)

# service items setup
display_settings = DisplaySettings(DEF_DATETIME_FMT)
weather_palette = Unicode256WeatherPalette()
icons_palette = Unicode256WeatherIconPalette()
w_painter = WeatherPainter(weather_palette)
i_painter = WeatherIconPainter(icons_palette)

# setup internal bus
subscribe_coloriser(CelsiusTemperature, w_painter, COLORISERS)
subscribe_coloriser(FarenheitTemperature, w_painter, COLORISERS)
subscribe_coloriser(WeatherIcon, i_painter, COLORISERS)

mode = DrawMode.FULLCOLOR
formatter = OpenweatherColorFormatter(COLORISERS, mode)
weather_service = OPW_WeatherService(OPENWEATHER_URL, UNITS)
weather_printer = CurrentWeatherPrinter(display_settings)
