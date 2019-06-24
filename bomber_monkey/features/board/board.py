import random
import time
from enum import Enum
from typing import Tuple

from python_ecs.ecs import Component


class Tiles(Enum):
    EMPTY = 0
    BLOCK = 1
    WALL = 2


class Board(Component):
    def __init__(self, grid_size: Tuple[int, int], tile_size: Tuple[int, int]) -> None:
        super().__init__()
        self.last_update = time.time()
        self.tile_size = tile_size
        self.grid_size = grid_size
        self.grid = [Tiles.EMPTY] * (grid_size[0] * grid_size[1])
        for i in range(25):
            x = random.randrange(2, self.width - 2)
            y = random.randrange(2, self.height - 2)
            self.set(x, y, Tiles.WALL)
        for i in range(50):
            x = random.randrange(2, self.width - 2)
            y = random.randrange(2, self.height - 2)
            self.set(x, y, Tiles.BLOCK)

        for x in range(self.width):
            self.set(x, 0, Tiles.WALL)
            self.set(x, self.height - 1, Tiles.WALL)
        for y in range(self.height):
            self.set(0, y, Tiles.WALL)
            self.set(self.width - 1, y, Tiles.WALL)

    @property
    def width(self):
        return self.grid_size[0]

    @property
    def height(self):
        return self.grid_size[1]

    def set(self, x: int, y: int, tile: Tiles):
        self.last_update = time.time()
        self.grid[self._index(x, y)] = tile

    def get(self, x: int, y: int) -> Tiles:
        return self.grid[self._index(x, y)]

    def grid_to_pixel(self, grid: Tuple[int, int]) -> Tuple[int, int]:
        return grid[0] * self.tile_size[0], grid[1] * self.tile_size[1]

    def pixel_to_grid(self, pixel: Tuple[int, int]) -> Tuple[int, int]:
        return pixel[0] // self.tile_size[0], pixel[1] // self.tile_size[1]

    def _index(self, x: int, y: int) -> int:
        return x + y * self.width

    def __repr__(self):
        return 'Board({},{})'.format(self.width, self.height)
