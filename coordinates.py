from dataclasses import dataclass
from subprocess import Popen, PIPE
from typing import Literal, Sequence, TypeAlias
import re

from exceptions import CantGetCoordinates


USE_ROUNDED_COORDS = False

Coordinate: TypeAlias = float


@dataclass(slots=True, frozen=True)
class Coordinates:
    latitude: Coordinate
    longitude: Coordinate


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
        output: Sequence[str],
        coord_type: Literal["latitude"] | Literal["longitude"]) -> Coordinate:
    pattern = _create_coord_str_pattern(coord_type)
    match_, matched_grp = None, None
    for line in output:
        match_ = pattern.match(line)
        if match_:
            matched_grp = match_.groupdict()
            return _parse_float_coordinate(matched_grp[coord_type])
    else:
        raise CantGetCoordinates


def _create_coord_str_pattern(coord_type: str) -> re.Pattern:
    head = f"^(.*)?(?:(?:{coord_type}))"
    tail = f"(.*)?(?P<{coord_type}>" + "(?:[0-9]{2}\.[0-9]{2,})).*$"  # noqa
    return re.compile(f"{head}{tail}")


def _parse_float_coordinate(value: str) -> Coordinate:
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
