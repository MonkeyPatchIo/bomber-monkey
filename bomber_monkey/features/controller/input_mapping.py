from abc import abstractmethod, ABC

from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.player.player_action import PlayerAction
from bomber_monkey.game_inputs import GameInputs
from python_ecs.ecs import Component, Simulator


class InputMapping(Component, ABC):
    @abstractmethod
    def get_action(self, inputs: GameInputs, menu: bool, sim: Simulator = None, body: RigidBody = None) -> PlayerAction:
        ...

    @property
    def type_id(self) -> 'Component.Type':
        return InputMapping
