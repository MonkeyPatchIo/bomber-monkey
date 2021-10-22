from typing import List

import numpy as np
from scipy.ndimage import convolve

from bomber_monkey.features.board.board import Cell, Tiles
from bomber_monkey.features.player.player_action import PlayerAction

K33 = np.array([
    [0, 1, 0],
    [1, 2, 1],
    [0, 1, 0],
]) / 8.


def feature_extractor(weights: List[float], kernel: np.ndarray = K33, loop=1):
    W = np.array(weights)[:, None, None]

    def extract(data: np.ndarray):
        feature = np.sum(data * W, axis=0)
        for _ in range(loop):
            feature = convolve(
                feature,
                kernel,
                mode='nearest',
                # cval=0
            )
        return feature

    return extract


def is_ignored(data: np.ndarray):
    return data.min() == data.max()


def choose(cell: Cell, data: np.ndarray):
    if is_ignored(data):
        return PlayerAction.NONE

    moves = {
        PlayerAction.NONE: cell,
        PlayerAction.MOVE_LEFT: cell.left(),
        PlayerAction.MOVE_RIGHT: cell.right(),
        PlayerAction.MOVE_UP: cell.up(),
        PlayerAction.MOVE_DOWN: cell.down()
    }
    moves = {
        k: v
        for k, v in moves.items()
        if v.tile == Tiles.EMPTY
    }

    best_move = max(moves, key=lambda k: data[moves[k].grid.y, moves[k].grid.x])
    if moves[best_move].tile != Tiles.EMPTY:
        return PlayerAction.NONE
    return best_move
