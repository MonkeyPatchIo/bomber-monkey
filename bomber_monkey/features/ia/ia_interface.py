from abc import ABC, abstractmethod

from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.player.player_action import PlayerAction
from python_ecs.ecs import Simulator


class IA(ABC):

    @abstractmethod
    def get_action(self, sim: Simulator, body: RigidBody) -> PlayerAction:
        ...
