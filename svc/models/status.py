from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from dataclasses_json import dataclass_json, config


_ISO_DATETIME = config(encoder=datetime.isoformat, decoder=datetime.fromisoformat)


@dataclass_json
@dataclass
class GarageCoordinates:
    latitude: float
    longitude: float


@dataclass_json
@dataclass
class GarageStatus:
    garageId: str
    isGarageOpen: bool
    duration: datetime = field(metadata=_ISO_DATETIME)
    coordinates: GarageCoordinates


@dataclass_json
@dataclass
class GarageDoorStatus:
    garageId: str
    isGarageOpen: bool
    duration: datetime = field(metadata=_ISO_DATETIME)


@dataclass_json
@dataclass
class AllGarageStatus:
    coordinates: GarageCoordinates
    doors: List[GarageDoorStatus]
