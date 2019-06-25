from bomber_monkey.features.physics.rigid_body import RigidBody
from python_ecs.ecs import System


class FrictionSystem(System):
    def __init__(self, ratio: float):
        super().__init__([RigidBody])
        self.ratio = ratio

    def update(self, body: RigidBody) -> None:
        body.speed *= self.ratio
