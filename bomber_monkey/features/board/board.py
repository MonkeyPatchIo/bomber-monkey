from typing import List

import numpy as np
import random
import time
from enum import IntEnum

from bomber_monkey.features.bomb.bomb import Bomb
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import Component, Entity


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
        bomb_grid = [None] * grid_size.x
        for _ in range(grid_size.x):
            bomb_grid[_] = [None] * grid_size.y
        self.bomb_grid: List[List[Entity]] = bomb_grid

    def on_create(self, entity: Entity):
        body: RigidBody = entity.get(RigidBody)
        bomb: Bomb = entity.get(Bomb)
        if bomb:
            self.by_pixel(body.pos).bomb = entity

    def on_destroy(self, entity: Entity):
        body: RigidBody = entity.get(RigidBody)
        bomb: Bomb = entity.get(Bomb)
        if bomb:
            self.by_pixel(body.pos).bomb = None

    def pixel_size(self) -> Vector:
        return self.tile_size.data * self.grid_size.data

    @property
    def width(self):
        return self.grid_size.x

    @property
    def height(self):
        return self.grid_size.y

    def by_pixel(self, pixel: Vector) -> 'Cell':
        grid = pixel // self.tile_size
        return self.by_grid(grid)

    def by_grid(self, grid: Vector) -> 'Cell':
        if grid.x < 0 or grid.y < 0 or grid.x >= self.width or grid.y >= self.height:
            return None
        return Cell(self, Vector.create(int(grid.x), int(grid.y)))

    def updated(self) -> None:
        self.last_update = time.time()

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
                board.by_grid(Vector.create(x, y)).tile = tile


def wall_grid(board: Board):
    for x in range(board.width):
        for y in range(board.height):
            if x % 2 == 0 and y % 2 == 0:
                board.by_grid(Vector.create(x, y)).tile = Tiles.WALL


class Cell:

    def __init__(self, board: Board, grid: Vector):
        self.board = board
        self.grid = grid

    def left(self) -> 'Cell':
        if self.grid.x == 0:
            return None
        return Cell(self.board, Vector.create(self.grid.x - 1, self.grid.y))

    def right(self) -> 'Cell':
        if self.grid.y == self.board.width - 1:
            return None
        return Cell(self.board, Vector.create(self.grid.x + 1, self.grid.y))

    def up(self) -> 'Cell':
        if self.grid.y == 0:
            return None
        return Cell(self.board, Vector.create(self.grid.x, self.grid.y - 1))

    def down(self) -> 'Cell':
        if self.grid.x == self.board.height - 1:
            return None
        return Cell(self.board, Vector.create(self.grid.x, self.grid.y + 1))

    def move(self, grid: Vector) -> 'Cell':
        new_grid = Vector.create(self.grid.x + grid.x, self.grid.y + grid.y)
        if new_grid.x < 0 or new_grid.y < 0 or new_grid.x >= self.board.width or new_grid.y >= self.board.height:
            return None
        return Cell(self.board, Vector.create(self.grid.x + grid.x, self.grid.y + grid.y))

    @property
    def bomb(self) -> Entity:
        return self.board.bomb_grid[int(self.grid.x)][int(self.grid.y)]

    @property
    def tile(self) -> Tiles:
        return Tiles(self.board.grid[int(self.grid.x), int(self.grid.y)])

    @bomb.setter
    def bomb(self, bomb: Entity):
        self.board.bomb_grid[int(self.grid.x)][int(self.grid.y)] = bomb

    @tile.setter
    def tile(self, tile: Tiles):
        self.board.grid[int(self.grid.x), int(self.grid.y)] = tile
        self.board.updated()

    @property
    def center(self) -> Vector:
        return self.grid * self.board.tile_size + (self.board.tile_size / 2)

    @property
    def top_left(self) -> Vector:
        return self.grid * self.board.tile_size

    def __repr__(self):
        return 'Cell[{}, {}]'.format(self.grid, self.tile)
