from dataclasses import dataclass
from datetime import datetime
from typing import List

from dataclasses_json import dataclass_json, cfg

cfg.global_config.encoders[datetime] = datetime.isoformat
cfg.global_config.decoders[datetime] = datetime.fromisoformat


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
    duration: datetime
    coordinates: GarageCoordinates


@dataclass_json
@dataclass
class GarageDoorStatus:
    garageId: str
    isGarageOpen: bool
    duration: datetime


@dataclass_json
@dataclass
class AllGarageStatus:
    coordinates: GarageCoordinates
    doors: List[GarageDoorStatus]
