from dataclasses import dataclass
from subprocess import Popen, PIPE
from typing import Literal
import re

from exceptions import CantGetCoordinates


USE_ROUNDED_COORDS = False


@dataclass(slots=True, frozen=True)
class Coordinates:
    latitude: float
    longitude: float


def get_gps_coordinates() -> Coordinates:
    """Returns current coordinates using MacBook GPS"""
    coordinates = _get_whereami_coordinates()
    return _round_coordinates(coordinates)


def _get_whereami_coordinates() -> Coordinates:
    whereami_output = _get_whereami_output()
    coordinates = _parse_coordinates(whereami_output)
    return coordinates


def _get_whereami_output() -> bytes:
    process = Popen(["whereami", "-r"], stdout=PIPE)
    output, err = process.communicate()
    exit_code = process.wait()
    if err is not None or exit_code != 0:
        raise CantGetCoordinates
    return output


def _parse_coordinates(whereami_output: bytes) -> Coordinates:
    try:
        output = whereami_output.decode().strip().lower().split("\n")
    except UnicodeDecodeError as err:
        raise CantGetCoordinates(err)
    return Coordinates(
        latitude=_parse_coord(output, "latitude"),
        longitude=_parse_coord(output, "longitude")
    )


def _parse_coord(
        output: list[str],
        coord_type: Literal["latitude"] | Literal["longitude"]) -> float:
    pattern = _create_coord_str_pattern(coord_type)
    for line in output:
        match_ = pattern.match(line)
        if match_:
            match_ = match_.groupdict()
            return _parse_float_coordinate(match_[coord_type])
    else:
        raise CantGetCoordinates


def _create_coord_str_pattern(coord_type: str) -> re.Pattern:
    head = f"^(.*)?(?:(?:{coord_type}))"
    tail = f"(.*)?(?P<{coord_type}>" + "(?:[0-9]{2}\.[0-9]{2,})).*$"
    return re.compile(f"{head}{tail}")


def _parse_float_coordinate(value: str) -> float:
    try:
        return float(value)
    except ValueError:
        raise CantGetCoordinates


def _round_coordinates(coordinates: Coordinates) -> Coordinates:
    if not USE_ROUNDED_COORDS:
        return coordinates
    return Coordinates(*map(
        lambda c: round(c, 3),
        [coordinates.latitude, coordinates.longitude]
    ))


if __name__ == "__main__":
    print(get_gps_coordinates())
