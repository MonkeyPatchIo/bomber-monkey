from enum import Enum, auto


class Feature(Enum):
    Threat = auto()
    BombTarget = auto()
    PickupTarget = auto()
    PathFinder = auto()
