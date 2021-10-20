from bomber_monkey.features.lifetime.lifetime import Lifetime
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.controller.input_mapping import InputMapping
from bomber_monkey.features.player.player_action import apply_action

from bomber_monkey.game_inputs import get_game_inputs
from python_ecs.ecs import System, Simulator


class ControllerSystem(System):

    def __init__(self):
        super().__init__([RigidBody, InputMapping])

    def update(self, sim: Simulator, dt: float, body: RigidBody, input_mapping: InputMapping):
        if sim.context.game_elapsed_time < sim.context.conf.game_startup_delay:
            return
        lifetime: Lifetime = body.entity().get(Lifetime)
        if lifetime is not None and lifetime.is_expiring():
            return

        action = input_mapping.get_action(get_game_inputs(), menu=False, sim=sim, body=body)
        apply_action(sim, action, body)
