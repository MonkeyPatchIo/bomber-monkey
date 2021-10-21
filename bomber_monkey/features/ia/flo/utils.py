from typing import Set, Iterator

from bomber_monkey.features.board.board import Cell, Board, Tiles
from bomber_monkey.features.bomb.explosion import ExplosionDirection
from bomber_monkey.features.player.player import Player
from bomber_monkey.utils.vector import Vector


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


def fire_cells_iter(board: Board, grid: Vector, direction: ExplosionDirection, bomb_size: int) -> Iterator[Vector]:
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


def attack_positions_iter(board: Board, self_player: Player) -> Iterator[Vector]:
    for eid, (player_pos, player) in board.state.players.items():
        if self_player.eid == eid:
            continue
        yield player_pos
        yield from fire_cells_iter(board, player_pos, ExplosionDirection.LEFT, self_player.power)
        yield from fire_cells_iter(board, player_pos, ExplosionDirection.RIGHT, self_player.power)
        yield from fire_cells_iter(board, player_pos, ExplosionDirection.UP, self_player.power)
        yield from fire_cells_iter(board, player_pos, ExplosionDirection.DOWN, self_player.power)


def danger_positions_iter(board: Board) -> Iterator[Vector]:
    for position, size, direction in board.state.explosions_iter():
        yield position
        if direction & ExplosionDirection.LEFT:
            yield from fire_cells_iter(board, position, ExplosionDirection.LEFT, size)
        if direction & ExplosionDirection.RIGHT:
            yield from fire_cells_iter(board, position, ExplosionDirection.RIGHT, size)
        if direction & ExplosionDirection.UP:
            yield from fire_cells_iter(board, position, ExplosionDirection.UP, size)
        if direction & ExplosionDirection.DOWN:
            yield from fire_cells_iter(board, position, ExplosionDirection.DOWN, size)
