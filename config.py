from settings import load_config
from weather_utils import (
        subscribe_coloriser,
        UnicodeWeatherKindIcons,
)
from colors import (
        Unicode256WeatherPalette,
        Unicode256WeatherIconsPalette,
        WeatherPainter,
        WeatherIconPainter,
        DrawMode,
)
from weather_models import (
        CelsiusTemperature,
        FarenheitTemperature,
)
from weather_formatter import OpenweatherColorFormatter
from weather_api_service import OPW_WeatherService
from view import DisplaySettings, CurrentWeatherPrinter


__all__ = [
        "formatter",
        "weather_service",
        "weather_printer",
        ]


app_config = load_config()

COLORISERS = {}
USE_ROUNDED_COORDS = False
UNITS = app_config["OPW_DEF_UNITS"]
OPENWEATHER_API = app_config["OPW_APIKEY"]
DEF_DATETIME_FMT = app_config["DATETIME_FMT"]
OPENWEATHER_URL = (
    "https://api.openweathermap.org/data/2.5/weather?"
    "lat={latitude}&lon={longitude}&"
    "appid=" + OPENWEATHER_API + f"&lang={app_config['OPW_DEF_LANG']}&"
    f"units={UNITS}"
)

# service items setup
display_settings = DisplaySettings(DEF_DATETIME_FMT)
weather_palette = Unicode256WeatherPalette()
icons_palette = Unicode256WeatherIconsPalette()
w_painter = WeatherPainter(weather_palette)
i_painter = WeatherIconPainter(icons_palette)

# setup internal bus
subscribe_coloriser(CelsiusTemperature, w_painter, COLORISERS)
subscribe_coloriser(FarenheitTemperature, w_painter, COLORISERS)
subscribe_coloriser(UnicodeWeatherKindIcons, i_painter, COLORISERS)

mode = DrawMode.FULLCOLOR
formatter = OpenweatherColorFormatter(COLORISERS, mode)
weather_service = OPW_WeatherService(OPENWEATHER_URL, UNITS)
weather_printer = CurrentWeatherPrinter(display_settings)
