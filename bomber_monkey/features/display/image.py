from typing import Tuple

import pygame as pg

from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import Component


class Image(Component):
    def __init__(self, path: str, size: Vector = None) -> None:
        super().__init__()
        self.path = path
        self.data = pg.image.load(path)
        if size:
            self.data = pg.transform.scale(self.data, size.data)

    def __repr__(self):
        return 'Image({})'.format(self.path)
