import time
from enum import IntEnum

from python_ecs.ecs import Component


class ExplosionDirection(IntEnum):
    UP = 1
    LEFT = 2
    RIGHT = 4
    DOWN = 8
    ALL = UP | LEFT | RIGHT | DOWN

    @staticmethod
    def opposed(direction: 'ExplosionDirection'):
        if direction == ExplosionDirection.UP:
            return ExplosionDirection.DOWN
        if direction == ExplosionDirection.DOWN:
            return ExplosionDirection.UP
        if direction == ExplosionDirection.LEFT:
            return ExplosionDirection.RIGHT
        if direction == ExplosionDirection.RIGHT:
            return ExplosionDirection.LEFT


class Explosion(Component):
    def __init__(self, direction: ExplosionDirection, power: int) -> None:
        super().__init__()
        self.direction = direction
        self.power = power
        self.propagated = False

    def __repr__(self):
        return 'Explosion({})'.format(self.direction)
