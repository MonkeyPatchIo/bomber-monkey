from enum import Enum, auto

import numpy as np

from bomber_monkey.features.board.board import Board, Tiles, Direction
from bomber_monkey.features.bomb.bomb import Bomb
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.player.player import Player
from bomber_monkey.utils.vector import Vector

SET_VALUE = 1


class BoardLayer(Enum):
    Empty = auto()
    Block = auto()
    Wall = auto()
    Bomb = auto()
    Explosion = auto()
    Banana = auto()
    Enemy = auto()

    def load(self, heatmap: np.ndarray, band: int, board: Board, player: Player):
        return self._get_loader()(heatmap, band, board, player)

    def _get_loader(self):
        mapping = {
            BoardLayer.Empty: empty_loader,
            BoardLayer.Block: block_loader,
            BoardLayer.Wall: wall_loader,
            BoardLayer.Bomb: bomb_loader,
            BoardLayer.Explosion: explosion_loader,
            BoardLayer.Banana: banana_loader,
            BoardLayer.Enemy: enemy_loader,
        }
        return mapping[self]


def empty_loader(heatmap: np.ndarray, band: int, board: Board, player: Player):
    for x in range(board.width):
        for y in range(board.height):
            if board.tile_grid[x, y] == Tiles.EMPTY:
                heatmap[band, y, x] = SET_VALUE


def block_loader(heatmap: np.ndarray, band: int, board: Board, player: Player):
    for x in range(board.width):
        for y in range(board.height):
            if board.tile_grid[x, y] == Tiles.BLOCK:
                heatmap[band, y, x] = SET_VALUE


def wall_loader(heatmap: np.ndarray, band: int, board: Board, player: Player):
    for x in range(board.width):
        for y in range(board.height):
            if board.tile_grid[x, y] == Tiles.WALL:
                heatmap[band, y, x] = SET_VALUE


def bomb_loader(heatmap: np.ndarray, band: int, board: Board, player: Player):
    for x in range(board.width):
        for y in range(board.height):
            cell = board.by_grid(Vector.create(x, y))
            for entity in cell.get(Bomb):
                bomb: Bomb = entity.get(Bomb)
                size = bomb.explosion_size + 1
                for dir in Direction:
                    for i, c in enumerate(cell.line(dir, 0, size)):
                        grad = 1.0 - i / size
                        heatmap[band, c.grid.y, c.grid.x] = SET_VALUE * grad
                        if c.tile != Tiles.EMPTY:
                            break


def explosion_loader(heatmap: np.ndarray, band: int, board: Board, player: Player):
    for (vec, item) in board.state.explosions.values():
        heatmap[band, vec.y, vec.x] = SET_VALUE


def banana_loader(heatmap: np.ndarray, band: int, board: Board, player: Player):
    for (vec, item) in board.state.bananas.values():
        heatmap[band, vec.y, vec.x] = SET_VALUE


def enemy_loader(heatmap: np.ndarray, band: int, board: Board, player: Player):
    for entity in board.players:
        if entity.get(Player) != player:
            pos = entity.get(RigidBody).pos
            cell = board.by_pixel(pos)
            heatmap[band, cell.grid.y, cell.grid.x] = SET_VALUE
    # for (vec, item) in board.state.players.values():
    #     if item != player:
    #         heatmap[band, vec.y, vec.x] = SET_VALUE
