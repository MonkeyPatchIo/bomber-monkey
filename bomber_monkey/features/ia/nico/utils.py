from enum import IntEnum
from typing import Set, Iterator

from bomber_monkey.features.board.board import Cell, Board, Tiles
from bomber_monkey.features.bomb.explosion import ExplosionDirection
from bomber_monkey.features.items.banana import Banana
from bomber_monkey.features.player.player import Player
from bomber_monkey.features.player.player_action import PlayerAction
from bomber_monkey.utils.vector import Vector


class IAGaol:
    def __init__(self, action: PlayerAction, description: str = "meh"):
        self.action = action
        self.description = description

    def __repr__(self) -> str:
        return f"{self.action}: {self.description}"


class IAGoalPath:
    def __init__(self, from_cell: Cell, next_cell: Cell, direction: ExplosionDirection, action: PlayerAction):
        self.from_cell = from_cell
        self.next_cell = next_cell
        self.direction = direction
        self.action = action


class TargetAction(IntEnum):
    STOP = 1
    GO = 2
    BOMB = 3
    CONTINUE = 4


def check_cell_content(cell: Cell, player: Player) -> TargetAction:
    if cell.tile == Tiles.WALL:
        return TargetAction.STOP
    for entity in cell.entities:
        if entity.get(Banana):
            return TargetAction.GO
    if cell.tile == Tiles.BLOCK:
        return TargetAction.BOMB
    return TargetAction.CONTINUE


def find_fire_cells(board: Board, grid: Vector, direction: ExplosionDirection, bomb_size: int) -> Iterator[Vector]:
    cell = board.by_grid(grid)
    while bomb_size > 0:
        if direction == ExplosionDirection.LEFT:
            cell = cell.left()
        elif direction == ExplosionDirection.RIGHT:
            cell = cell.right()
        elif direction == ExplosionDirection.UP:
            cell = cell.up()
        elif direction == ExplosionDirection.DOWN:
            cell = cell.down()
        if cell.tile in [Tiles.WALL, Tiles.BLOCK]:
            return
        bomb_size = bomb_size - 1
        yield cell.grid


def find_attack_positions(board: Board, self_player: Player) -> Iterator[Vector]:
    for eid, (player_pos, player) in board.state.players.items():
        if self_player.eid == eid:
            continue
        yield player_pos
        yield from find_fire_cells(board, player_pos, ExplosionDirection.LEFT, self_player.power)
        yield from find_fire_cells(board, player_pos, ExplosionDirection.RIGHT, self_player.power)
        yield from find_fire_cells(board, player_pos, ExplosionDirection.UP, self_player.power)
        yield from find_fire_cells(board, player_pos, ExplosionDirection.DOWN, self_player.power)


def find_danger_positions(board: Board) -> Iterator[Vector]:
    for position, size, direction in board.state.explosions_iter():
        yield position
        if direction & ExplosionDirection.LEFT:
            yield from find_fire_cells(board, position, ExplosionDirection.LEFT, size)
        if direction & ExplosionDirection.RIGHT:
            yield from find_fire_cells(board, position, ExplosionDirection.RIGHT, size)
        if direction & ExplosionDirection.UP:
            yield from find_fire_cells(board, position, ExplosionDirection.UP, size)
        if direction & ExplosionDirection.DOWN:
            yield from find_fire_cells(board, position, ExplosionDirection.DOWN, size)


def walk_next(visited_positions: Set[Vector], cell: Cell, direction: ExplosionDirection):
    if direction != ExplosionDirection.RIGHT:
        next_cell = cell.left()
        if next_cell.grid not in visited_positions:
            yield next_cell, ExplosionDirection.LEFT
    if direction != ExplosionDirection.LEFT:
        next_cell = cell.right()
        if next_cell.grid not in visited_positions:
            yield next_cell, ExplosionDirection.RIGHT
    if direction != ExplosionDirection.DOWN:
        next_cell = cell.up()
        if next_cell.grid not in visited_positions:
            yield next_cell, ExplosionDirection.UP
    if direction != ExplosionDirection.UP:
        next_cell = cell.down()
        if next_cell.grid not in visited_positions:
            yield next_cell, ExplosionDirection.DOWN
