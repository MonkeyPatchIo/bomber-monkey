from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.destruction.destruction import Destruction, Protection
from bomber_monkey.game_factory import GameFactory
from bomber_monkey.utils.collision_detector import detect_collision
from python_ecs.ecs import System


class ProtectionSystem(System):

    def __init__(self):
        super().__init__([Protection])

    def update(self, dt: float, protection: Protection) -> None:
        protection.remaining -= dt
