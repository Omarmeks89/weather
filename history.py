from datetime import datetime
import json
from pathlib import Path
from typing import TypedDict, Protocol

from weather_models import WeatherModel
from weather_formatter import format_weather
from exceptions import StorageError


class WeatherStorage(Protocol):
    """Interface for any storage saving weather"""
    def save(self, weather: WeatherModel) -> None:
        raise NotImplementedError


class PlainFileWeatherStorage:
    """Store weather in plain text file"""
    def __init__(self, file: Path) -> None:
        self._file = file

    def save(self, weather: WeatherModel) -> None:
        now = datetime.now()
        formatted_weather = format_weather(weather)
        try:
            with open(self._file, "a") as f:
                f.write(f"{now}\n{formatted_weather}\n")
        except FileNotFoundError as err:
            raise StorageError from err


class HistoryRecord(TypedDict):
    date: str
    weather: str


class JSONFileWeatherStorage:
    """Store weather in JSON file"""
    def __init__(self, jsonfile: Path) -> None:
        self._jsonfile = jsonfile
        self._init_storage()

    def save(self, weather: WeatherModel) -> None:
        history: HistoryRecord = {
            "date": str(datetime.now()),
            "weather": format_weather(weather)
        }
        self._write(history)

    def _init_storage(self) -> None:
        if not self._jsonfile.exists():
            self._jsonfile.write_text("[Metadata section...]")

    def _read_history(self) -> list[HistoryRecord]:
        try:
            with open(self._jsonfile, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            raise StorageError

    def _write(self, history: HistoryRecord) -> None:
        """If we would have a+ or a mode we`ll have err."""
        try:
            with open(self._jsonfile, "a+") as f:
                json.dump(history, f, ensure_ascii=False, indent=4)
        except FileNotFoundError:
            raise StorageError


def save_weather(weather: WeatherModel, storage: WeatherStorage) -> None:
    """Saves weather in the storage"""
    storage.save(weather)
