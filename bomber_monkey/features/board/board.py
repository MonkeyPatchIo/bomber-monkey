import random
from enum import Enum

from python_ecs.ecs import Component


class Tiles(Enum):
    EMPTY = 0
    BLOCK = 1
    WALL = 2


class Board(Component):
    def __init__(self, width: int, height: int) -> None:
        super().__init__()
        self.width = width
        self.height = height
        self.grid = [Tiles.EMPTY] * (width * height)
        for i in range(10):
            index = random.randint(0, len(self.grid)-1)
            self.grid[index] = Tiles.WALL
        for i in range(10):
            index = random.randint(0, len(self.grid))
            self.grid[index] = Tiles.BLOCK

    def set(self, x: int, y: int, tile: Tiles):
        self.grid[self._index(x, y)] = tile

    def get(self, x: int, y: int) -> Tiles:
        return self.grid[self._index(x, y)]

    def _index(self, x: int, y: int) -> int:
        return x + y * self.width

    def __repr__(self):
        return 'Board({},{})'.format(self.width, self.height)
