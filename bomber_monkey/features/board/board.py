import numpy as np
import random
import time
from enum import IntEnum

from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import Component


class Tiles(IntEnum):
    EMPTY = 0
    BLOCK = 1
    WALL = 2


class Board(Component):
    def __init__(self, grid_size: Vector, tile_size: Vector) -> None:
        super().__init__()
        self.last_update = time.time()
        self.tile_size = tile_size
        self.grid_size = grid_size
        self.grid = np.zeros(grid_size.data)

    @property
    def pixel_size(self) -> Vector:
        return self.tile_size.data * self.grid_size.data

    @property
    def width(self):
        return self.grid_size.x

    @property
    def height(self):
        return self.grid_size.y

    def set(self, x: int, y: int, tile: Tiles):
        self.last_update = time.time()
        self.grid[int(x), int(y)] = tile.value

    def get(self, x: int, y: int) -> Tiles:
        return Tiles(self.grid[int(x), int(y)])

    def to_grid_center(self, pixel: Vector) -> Vector:
        """

        :param pixel: coordinate in pixel
        :return: the same pixel coordinate centered in its grid tile
        """
        grid = self.pixel_to_grid(pixel)
        center = self.grid_to_pixel_center(grid)
        return center

    def grid_to_pixel_center(self, grid: Vector) -> Vector:
        return grid * self.tile_size + self.tile_size // 2

    def pixel_to_grid(self, pixel: Vector) -> Vector:
        return pixel // self.tile_size

    def __repr__(self):
        return 'Board({},{})'.format(self.width, self.height)


def fill_border(board: Board, tile: Tiles):
    board.grid[0, :] = board.grid[-1, :] = tile.value
    board.grid[:, 0] = board.grid[:, -1] = tile.value


def clear_corners(board: Board):
    board.grid[:3, :3] = board.grid[-3:, :3] = Tiles.EMPTY.value
    board.grid[:3, -3:] = board.grid[-3:, -3:] = Tiles.EMPTY.value


def random_blocks(board: Board, tile: Tiles, ratio: float):
    for x in range(board.width):
        for y in range(board.height):
            if random.random() < ratio:
                board.set(x, y, tile)
