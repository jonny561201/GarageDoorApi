from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class GarageCoordinates:
    latitude: float
    longitude: float


@dataclass_json
@dataclass
class GarageStatus:
    isGarageOpen: bool
    statusDuration: str
    coordinates: GarageCoordinates