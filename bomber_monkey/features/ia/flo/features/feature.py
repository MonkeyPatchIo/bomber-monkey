from enum import Enum, auto


class Feature(Enum):
    PathFinder = auto()
    BombTarget = auto()
    PickupTarget = auto()
    Threat = auto()
