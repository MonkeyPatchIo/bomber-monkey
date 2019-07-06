from typing import List

import numpy as np
import random
import time
from enum import IntEnum

from bomber_monkey.features.banana.banana import Banana
from bomber_monkey.features.bomb.bomb import Bomb
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.player.player import Player
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

        self.bomb_grid = self._init_grid()
        self.banana_grid = self._init_grid()
        self.player_grid = self._init_grid()
        self._players = []

    def update_pos(self, last_pos: Vector, body: RigidBody):
        entity = body.entity()
        new_pos = body.pos
        if entity.get(Player):
            self.by_pixel(last_pos).player = None
            self.by_pixel(new_pos).player = entity
        if entity.get(Banana):
            self.by_pixel(last_pos).banana = None
            self.by_pixel(new_pos).banana = entity
        if entity.get(Bomb):
            self.by_pixel(last_pos).bomb = None
            self.by_pixel(new_pos).bomb = entity

    @property
    def players(self):
        return self._players

    def _init_grid(self) -> List[List[Entity]]:
        grid = [None] * self.grid_size.x
        for _ in range(self.grid_size.x):
            grid[_] = [None] * self.grid_size.y
        return grid

    def on_create(self, entity: Entity):
        body: RigidBody = entity.get(RigidBody)
        bomb: Bomb = entity.get(Bomb)
        banana: Banana = entity.get(Banana)
        player: Player = entity.get(Player)

        if bomb:
            self.by_pixel(body.pos).bomb = entity
        if banana:
            self.by_pixel(body.pos).banana = entity
        if player:
            self.by_pixel(body.pos).player = entity
            self._players.append(entity)

    def on_destroy(self, entity: Entity):
        body: RigidBody = entity.get(RigidBody)
        bomb: Bomb = entity.get(Bomb)
        banana: Banana = entity.get(Banana)
        player: Player = entity.get(Player)

        if bomb:
            self.by_pixel(body.pos).bomb = None
        if banana:
            self.by_pixel(body.pos).banana = None
        if player:
            self.by_pixel(body.pos).player = None
            self._players.remove(entity)

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


def clear_center(board: Board):
    board.grid[5:-5, 4:-4] = Tiles.EMPTY.value


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

    @bomb.setter
    def bomb(self, bomb: Entity):
        self.board.bomb_grid[int(self.grid.x)][int(self.grid.y)] = bomb

    @property
    def banana(self) -> Entity:
        return self.board.banana_grid[int(self.grid.x)][int(self.grid.y)]

    @banana.setter
    def banana(self, banana: Entity):
        self.board.banana_grid[int(self.grid.x)][int(self.grid.y)] = banana

    @property
    def player(self) -> Entity:
        return self.board.player_grid[int(self.grid.x)][int(self.grid.y)]

    @player.setter
    def player(self, player: Entity):
        self.board.player_grid[int(self.grid.x)][int(self.grid.y)] = player

    @property
    def tile(self) -> Tiles:
        return Tiles(self.board.grid[int(self.grid.x), int(self.grid.y)])

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
