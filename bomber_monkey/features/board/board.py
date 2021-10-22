import random
import time
from enum import IntEnum, Enum, auto
from typing import List, Set, Optional, Iterator, Union

import numpy as np

from bomber_monkey.features.board.board_state import BoardState
from bomber_monkey.features.board.board_update import BoardUpdate
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

        self.tile_grid = np.zeros(grid_size.data)
        self.entity_grid = self._init_grid()

        self._players = []
        self.updates: List[BoardUpdate] = []
        self.state = BoardState()

    def update_pos(self, last_pos: Vector, body: RigidBody):
        new_pos = body.pos
        if last_pos != new_pos:
            last_cell = self.by_pixel(last_pos)
            new_cell = self.by_pixel(new_pos)
            if last_cell.grid != new_cell.grid:
                entity = body.entity()
                last_cell.entities.remove(entity)
                new_cell.entities.add(entity)
                self.updates.append(BoardUpdate(False, last_cell.grid, entity))
                self.updates.append(BoardUpdate(True, new_cell.grid, entity))

    @property
    def players(self):
        return self._players

    def _init_grid(self) -> List[List[Set[Entity]]]:
        grid = [None] * self.grid_size.x
        for _ in range(self.grid_size.x):
            grid[_] = [None] * self.grid_size.y
            for y in range(self.grid_size.y):
                grid[_][y] = set()
        return grid

    def on_create(self, entity: Entity):
        body: RigidBody = entity.get(RigidBody)
        player: Player = entity.get(Player)

        if body:
            cell = self.by_pixel(body.pos)
            cell.entities.add(entity)
            self.updates.append(BoardUpdate(True, cell.grid, entity))
        if player:
            self._players.append(entity)

    def on_destroy(self, entity: Entity):
        body: RigidBody = entity.get(RigidBody)
        player: Player = entity.get(Player)

        if body:
            cell = self.by_pixel(body.pos)
            cell.entities.remove(entity)
            self.updates.append(BoardUpdate(False, cell.grid, entity))
        if player:
            self._players.remove(entity)

    def pixel_size(self) -> Vector:
        return self.tile_size * self.grid_size

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

    def by_relative_grid(self, relative_grid: Vector) -> 'Cell':
        grid = Vector.create(relative_grid.x, relative_grid.y)
        if relative_grid.x < 0:
            grid.x = self.width - 1 + relative_grid.x
        if relative_grid.y < 0:
            grid.y = self.height - 1 + relative_grid.y
        return self.by_grid(grid)

    def updated(self) -> None:
        self.last_update = time.time()

    def __repr__(self):
        return 'Board({},{})'.format(self.width, self.height)


def fill_board(board: Board):
    random_blocks(board, Tiles.BLOCK, 1.)
    # random_blocks(board, Tiles.WALL, .5)
    clear_corners(board)
    clear_center(board)

    wall_grid(board)

    fill_border(board, Tiles.WALL)


def fill_border(board: Board, tile: Tiles):
    board.tile_grid[0, :] = board.tile_grid[-1, :] = tile.value
    board.tile_grid[:, 0] = board.tile_grid[:, -1] = tile.value


def clear_corners(board: Board):
    board.tile_grid[:3, :3] = board.tile_grid[-3:, :3] = Tiles.EMPTY.value
    board.tile_grid[:3, -3:] = board.tile_grid[-3:, -3:] = Tiles.EMPTY.value


def clear_center(board: Board):
    board.tile_grid[5:-5, 4:-4] = Tiles.EMPTY.value


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


class Direction(Enum):
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()


class Cell:

    def __init__(self, board: Board, grid: Vector):
        self.board = board
        self.grid = grid

    def line(self, direction: Direction, skip: int, length: int):
        curr = self
        yield curr
        for i in range(skip, length):
            curr = curr.go(direction)
            if curr is None:
                return
            yield curr

    def go(self, direction: Direction) -> 'Optional[Cell]':
        mapping = {
            Direction.NORTH: self.up,
            Direction.SOUTH: self.down,
            Direction.EAST: self.right,
            Direction.WEST: self.left,
        }
        return mapping[direction]()

    def left(self) -> 'Optional[Cell]':
        if self.grid.x == 0:
            return None
        return Cell(self.board, Vector.create(self.grid.x - 1, self.grid.y))

    def right(self) -> 'Optional[Cell]':
        if self.grid.x == self.board.width - 1:
            return None
        return Cell(self.board, Vector.create(self.grid.x + 1, self.grid.y))

    def up(self) -> 'Optional[Cell]':
        if self.grid.y == 0:
            return None
        return Cell(self.board, Vector.create(self.grid.x, self.grid.y - 1))

    def down(self) -> 'Optional[Cell]':
        if self.grid.y == self.board.height - 1:
            return None
        return Cell(self.board, Vector.create(self.grid.x, self.grid.y + 1))

    def move(self, grid: Vector) -> 'Optional[Cell]':
        new_grid = Vector.create(self.grid.x + grid.x, self.grid.y + grid.y)
        if new_grid.x < 0 or new_grid.y < 0 or new_grid.x >= self.board.width or new_grid.y >= self.board.height:
            return None
        return Cell(self.board, Vector.create(self.grid.x + grid.x, self.grid.y + grid.y))

    @property
    def entities(self) -> Set[Entity]:
        return self.board.entity_grid[int(self.grid.x)][int(self.grid.y)]

    def get(self, *c_type: Union[Component.Type, List[Component.Type]]) -> Iterator[Entity]:
        def test(entity: Entity):
            for _ in c_type:
                if entity.get(_) is not None:
                    return True
            return False

        return filter(test, self.entities)

    @property
    def has_bomb(self):
        return len(list(self.get(Bomb))) > 0

    @property
    def tile(self) -> Tiles:
        return Tiles(self.board.tile_grid[int(self.grid.x), int(self.grid.y)])

    @tile.setter
    def tile(self, tile: Tiles):
        self.board.tile_grid[int(self.grid.x), int(self.grid.y)] = tile
        self.board.updated()

    @property
    def center(self) -> Vector:
        return self.grid * self.board.tile_size + (self.board.tile_size / 2)

    @property
    def top_left(self) -> Vector:
        return self.grid * self.board.tile_size

    def __repr__(self):
        return f"{self.grid}, {self.tile}"

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Cell):
            return self.grid == other.grid
        return False

    def __hash__(self):
        return hash(self.grid)
