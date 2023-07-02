# interfaces for coods fetching
from abc import ABC, abstractmethod
from typing import NoReturn

from coordinates import Coordinates


class AbstractGPSGrabber(ABC):
    """GPS grabber interface."""

    @abstractmethod
    def get_gps_coordinates() -> NoReturn:
        pass

    @staticmethod
    @abstractmethod
    def round_coordinates(coordinates: Coordinates) -> NoReturn:
        pass


class WhereamiGPSGrabber(AbstractGPSGrabber):
    pass
