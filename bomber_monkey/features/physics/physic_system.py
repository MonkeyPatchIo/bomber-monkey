import numpy as np

from bomber_monkey.features.physics.rigid_body import RigidBody
from python_ecs.ecs import System


class PhysicSystem(System):
    def __init__(self, friction_ratio: float):
        super().__init__([RigidBody])
        self.friction = friction_ratio

    def update(self,dt: float,  body: RigidBody) -> None:
        body.speed += body.accel
        body.pos += body.speed

        body.speed *= self.friction
        if np.linalg.norm(body.speed.data) < .5:
            body.speed *= 0
