from bomber_monkey.features.lifetime.lifetime import Lifetime
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.player.player_action import InputMapping, PlayerAction, apply_action

from bomber_monkey.game_inputs import GameInputs
from python_ecs.ecs import System, Simulator


class IA:
    def get_action(self, sim: Simulator, body: RigidBody) -> PlayerAction:
        pass


class IAMapping(InputMapping):

    def __init__(self, ia: IA):
        super().__init__()
        self.ia = ia

    def get_action(self, inputs: GameInputs, menu: bool) -> PlayerAction:
        return PlayerAction.NONE



class IAControllerSystem(System):

    def __init__(self):
        super().__init__([RigidBody, IAMapping])

    def update(self, sim: Simulator, dt: float, body: RigidBody, ia_mapping: IAMapping):
        if sim.context.game_elapsed_time < sim.context.conf.game_startup_delay:
            return
        lifetime: Lifetime = body.entity().get(Lifetime)
        if lifetime is not None and lifetime.is_expiring():
            return

        action = ia_mapping.ia.get_action(sim, body)
        apply_action(sim, action, body)
