import pygame as pg

from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import Component


class Image(Component):
    def __init__(self, path: str, size: Vector = None) -> None:
        super().__init__()
        self.path = path
        self.size = size

    def __eq__(self, other):
        if isinstance(other, Image):
            return self.path == other.path and self.size == other.size
        return False

    def __hash__(self):
        return hash((self.path, self.size))

    def __repr__(self):
        return 'Image({})'.format(self.path)
