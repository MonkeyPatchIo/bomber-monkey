from abc import ABC, abstractmethod

from bomber_monkey.features.board.board import Board
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.player.player_action import PlayerAction


class IA(ABC):

    @abstractmethod
    def get_action(self, board: Board, body: RigidBody) -> PlayerAction:
        ...
