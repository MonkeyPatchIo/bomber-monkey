import numpy as np

from bomber_monkey.features.board.board import Board
from bomber_monkey.features.ia.ia_interface import IA
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.player.player import Player
from bomber_monkey.features.player.player_action import PlayerAction


class Heatmap:
    def __init__(self, board: Board):
        layers = [
            'Blocked',
            'Bomb',
            'Explosion',
            'Banana',
        ]
        depth = len(layers)
        self.heatmap = np.zeros((board.height, board.width, depth))


class FloIA(IA):
    def __init__(self):
        super().__init__()

    def get_action(self, board: Board, body: RigidBody) -> PlayerAction:
        player: Player = body.entity().get(Player)
        state = board.state

        body_cell = board.by_pixel(body.pos)
        goal = self.find_action(board, body_cell, player)
        self.current_goal = goal
        return goal.action
