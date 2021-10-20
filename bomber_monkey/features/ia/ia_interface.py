from abc import ABC, abstractmethod

from bomber_monkey.features.ia.flo.board_state import BoardState
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.player.player_action import PlayerAction
from python_ecs.ecs import Simulator


class IA(ABC):
    _state = BoardState()

    @property
    def state(self):
        return self._state

    @abstractmethod
    def get_action(self, sim: Simulator, body: RigidBody) -> PlayerAction:
        ...
