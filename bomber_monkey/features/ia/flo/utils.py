import numpy as np
from scipy.ndimage import convolve

from bomber_monkey.features.board.board import Cell, Tiles
from bomber_monkey.features.player.player_action import PlayerAction

K33 = np.array([
    [0, 1, 0],
    [1, 4, 1],
    [0, 1, 0],
]) / 8.


def feature_extractor(weights: dict, kernel: np.ndarray = K33):
    W = .001 * np.array(list(weights.values()))[:, None, None]

    def extract(data: np.ndarray, n: int = 1):
        feature = np.sum(data * W, axis=0)
        for _ in range(n):
            feature = convolve(feature, kernel, mode='constant', cval=0)
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

    best_move = max(moves, key=lambda k: data[moves[k].grid.x, moves[k].grid.y])
    if moves[best_move].tile != Tiles.EMPTY:
        return PlayerAction.NONE
    return best_move
