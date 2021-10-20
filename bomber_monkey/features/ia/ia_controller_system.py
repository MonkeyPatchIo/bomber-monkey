from bomber_monkey.features.ia.ia_mapping import IAMapping
from bomber_monkey.features.lifetime.lifetime import Lifetime
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.player.player_action import apply_action
from bomber_monkey.utils.timing import timing
from python_ecs.ecs import System, Simulator


class IAControllerSystem(System):
    def __init__(self):
        super().__init__([RigidBody, IAMapping])

    def update(self, sim: Simulator, dt: float, body: RigidBody, ia_mapping: IAMapping):
        if sim.context.game_elapsed_time < sim.context.conf.game_startup_delay:
            return
        lifetime: Lifetime = body.entity().get(Lifetime)
        if lifetime is not None and lifetime.is_expiring():
            return

        with timing(f'{ia_mapping.ia.__class__.__name__}[{hash(ia_mapping.ia)}].update'):
            action = ia_mapping.ia.get_action(sim, body)
        apply_action(sim, action, body)
