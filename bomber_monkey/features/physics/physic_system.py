from typing import Tuple

import numpy as np

from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import System


class PhysicSystem(System):
    def __init__(self, friction_ratio: float):
        super().__init__([RigidBody])
        self.friction = friction_ratio

    def update(self, dt: float, body: RigidBody) -> None:
        body.pos, body.speed = self.next_state(body, dt)

        body.speed *= self.friction * dt
        if np.linalg.norm(body.speed.data) < .5 * dt:
            body.speed *= 0

    @staticmethod
    def next_state(body: RigidBody, dt: float) -> Tuple[Vector, Vector]:
        next_speed = body.speed + body.accel * dt
        next_pos = body.pos + next_speed * dt
        return next_pos, next_speed
