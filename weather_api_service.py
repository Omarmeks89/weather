from datetime import datetime
import json
from json.decoder import JSONDecodeError
import ssl
from typing import Literal
import urllib.request
from urllib.error import URLError
from abc import ABC, abstractmethod
from typing import TypeAlias, Union

from coordinates import Coordinates

from exceptions import ApiServiceError
from weather_models import (
        WeatherModel,
        WeatherDescription,
        BaseTemperature,
        CelsiusTemperature,
        FarenheitTemperature,
)
from weather_utils import TemperatureScaleKind
from base_types import NumericArg


_Numeric: TypeAlias = Union[int, float]
_Literal: TypeAlias = Union[str, bytes]


class ExternalWeatherService(ABC):

    def __init__(
            self,
            url: str,
            units: Literal["metric"] | Literal["imperial"],
            ) -> None:
        self._url = url
        self._units = units
        if self._units == "metric":
            self._tmpr_scale = TemperatureScaleKind.CELSIUS
        else:
            self._tmpr_scale = TemperatureScaleKind.FARENHEIT

    def get_weather(self, coordinates: Coordinates) -> WeatherModel:
        response = self._get_weather_service_response(
                latitude=coordinates.latitude,
                longitude=coordinates.longitude
                )
        weather = self._parse_weather_service_response(response)
        return weather

    def _get_weather_service_response(
            self,
            latitude: _Numeric,
            longitude: _Numeric,
            ) -> _Literal:
        ssl._create_default_https_context = ssl._create_unverified_context
        url = self._url.format(latitude=latitude, longitude=longitude)
        try:
            return urllib.request.urlopen(url).read()
        except URLError:
            raise ApiServiceError

    def _parse_weather_service_response(self, resp: _Literal) -> WeatherModel:
        try:
            openweather_dict = json.loads(resp)
        except JSONDecodeError:
            raise ApiServiceError
        return WeatherModel(
            temperature=self._get_temperature(openweather_dict),
            weather_type=self._parse_weather_descr(openweather_dict),
            sunrise=self._parse_sun_time(openweather_dict, "sunrise"),
            sunset=self._parse_sun_time(openweather_dict, "sunset"),
            city=self._parse_city(openweather_dict)
        )

    @abstractmethod
    def _get_temperature(self, data_src: dict) -> BaseTemperature:
        pass

    @abstractmethod
    def _parse_weather_descr(self, data_src: dict) -> WeatherDescription:
        pass

    @abstractmethod
    def _parse_sun_time(
            self,
            data_src: dict,
            time: Literal["sunrise"] | Literal["sunset"],
            ) -> datetime:
        pass

    @abstractmethod
    def _parse_city(self, data_src: dict) -> _Literal:
        pass


class OPW_WeatherService(ExternalWeatherService):

    def _get_temperature(self, data_src: dict) -> BaseTemperature:
        """set via WeatherArg -> NumericArg."""
        temperature = self._convert_temperature_to_weather_arg(
                data_src["main"]["temp"],
                )
        if self._tmpr_scale is TemperatureScaleKind.CELSIUS:
            return CelsiusTemperature(temperature)
        return FarenheitTemperature(temperature)

    def _convert_temperature_to_weather_arg(value: _Numeric) -> NumericArg:
        return NumericArg(round(value))

    def _parse_weather_descr(self, data_src: dict) -> WeatherDescription:
        try:
            weather_type = data_src["weather"][0]["main"]
            weather_descr = data_src["weather"][0]["description"]
            return WeatherDescription(
                    main=weather_type,
                    description=weather_descr,
            )
        except (KeyError, IndexError) as err:
            raise ApiServiceError(err)

    def _parse_sun_time(
            self,
            data_src: dict,
            time: Literal["sunrise"] | Literal["sunset"],
            ) -> datetime:
        return datetime.fromtimestamp(data_src["sys"][time])

    def _parse_city(self, data_src: dict) -> _Literal:
        try:
            return data_src["name"]
        except KeyError:
            raise ApiServiceError
