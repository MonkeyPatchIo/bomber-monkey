import numpy as np
from scipy.ndimage import convolve

from bomber_monkey.features.board.board import Board, Cell
from bomber_monkey.features.ia.flo.heatmap import Heatmap
from bomber_monkey.features.ia.ia_interface import IA
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.player.player import Player
from bomber_monkey.features.player.player_action import PlayerAction

MOVE_TARGET = {
    'Empty': 2,
    'Block': 2,
    'Wall': -1,
    'Bomb': -20,
    'Explosion': -100,
    'Banana': 8,
    'Enemy': 4,
}

BOMB_TARGET = {
    'Empty': 0,
    'Block': 2,
    'Wall': -1,
    'Bomb': -5,
    'Explosion': -100,
    'Banana': -2,
    'Enemy': 50,
}

move_weights = .001 * np.array(list(MOVE_TARGET.values()))[:, None, None]
bomb_weights = .001 * np.array(list(BOMB_TARGET.values()))[:, None, None]
move_kernel = np.array([
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [1, 1, 1, 1, 1],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
])
bomb_kernel = np.array([
    [0, 0, 1, 0, 0],
    [0, 1, 5, 1, 0],
    [1, 5, 0, 5, 1],
    [0, 1, 5, 1, 0],
    [0, 0, 1, 0, 0],
])


class FloIA(IA):
    def __init__(self):
        super().__init__()
        self.heatmap = Heatmap()

        self.target: np.ndarray = None

    def get_action(self, board: Board, body: RigidBody) -> PlayerAction:
        player: Player = body.entity().get(Player)
        cell: Cell = board.by_pixel(body.pos)
        self.heatmap.load_board(board, player)

        move_target = np.sum(self.heatmap.heatmap * move_weights, axis=0)
        bomb_target = np.sum(self.heatmap.heatmap * bomb_weights, axis=0)

        move_target2 = convolve(move_target, move_kernel, mode='constant', cval=0)
        bomb_target2 = convolve(bomb_target, bomb_kernel, mode='constant', cval=0)

        moves = {
            PlayerAction.NONE: cell,
            PlayerAction.MOVE_LEFT: cell.left(),
            PlayerAction.MOVE_RIGHT: cell.right(),
            PlayerAction.MOVE_UP: cell.up(),
            PlayerAction.MOVE_DOWN: cell.down()
        }

        best_move = max(moves, key=lambda k: move_target2[moves[k].grid.x, moves[k].grid.y])
        bomb = bomb_target2[cell.grid.x, cell.grid.y]
        if best_move == PlayerAction.NONE and bomb > 0:
            return PlayerAction.MAIN_ACTION

        return best_move
