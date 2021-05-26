from bomber_monkey.features.lifetime.lifetime import Lifetime
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.player.player_action import apply_action
from bomber_monkey.features.player.user_input_mapping import UserInputMapping

from bomber_monkey.game_config import GameConfig
from bomber_monkey.game_inputs import get_game_inputs
from python_ecs.ecs import System, Simulator


class UserControllerSystem(System):

    def __init__(self):
        super().__init__([RigidBody, UserInputMapping])

    def update(self, sim: Simulator, dt: float, body: RigidBody, input_mapping: UserInputMapping):
        if sim.context.game_elapsed_time < sim.context.conf.game_startup_delay:
            return
        lifetime: Lifetime = body.entity().get(Lifetime)
        if lifetime is not None and lifetime.is_expiring():
            return

        conf: GameConfig = sim.context.conf

        action = input_mapping.get_action(get_game_inputs(), menu=False)
        apply_action(sim, action, body, conf)