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


class Sprite(Image):
    def __init__(self, path: str, sprite_size: Vector, anim_size: int, size: Vector = None) -> None:
        super().__init__(path, size)
        self.sprite_size = sprite_size
        self.anim_size = anim_size
        self.current = 0

    def __repr__(self):
        return 'Sprite({})'.format(self.path)
