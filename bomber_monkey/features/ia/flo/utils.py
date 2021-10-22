from typing import List

import numpy as np

from bomber_monkey.features.board.board import Cell
from bomber_monkey.features.player.player_action import PlayerAction

K33 = np.array([
    [0, 1, 0],
    [1, 2, 1],
    [0, 1, 0],
]) / 8.


def feature_extractor(weights: List[float], kernel: np.ndarray = K33, loop=1):
    from scipy.ndimage import convolve

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


def choose(
        cell: Cell,
        data: np.ndarray,
        treshold: float = None
):
    if is_ignored(data):
        return None

    moves = {
        PlayerAction.NONE: cell,
        PlayerAction.MOVE_LEFT: cell.left(),
        PlayerAction.MOVE_RIGHT: cell.right(),
        PlayerAction.MOVE_UP: cell.up(),
        PlayerAction.MOVE_DOWN: cell.down()
    }
    valued_moves = {
        k: (c, data[c.grid.y, c.grid.x])
        for k, c in moves.items()
        # if c.tile == Tiles.EMPTY
    }
    valued_moves = {
        k: v
        for k, v in valued_moves.items()
        if treshold is None or v[1] > treshold
    }
    if len(valued_moves) == 0:
        return None

    best_move = max(valued_moves, key=lambda k: valued_moves[k][1])
    return best_move


def normalize(data: np.ndarray):
    a, b = data.min(), data.max()
    if a == b:
        return data
    return (data - a) / (b - a)