from typing import Tuple

import numpy as np

from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.game_factory import GameFactory
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import System, Simulator


class PhysicSystem(System):
    def __init__(self, factory: GameFactory, friction_ratio: float):
        super().__init__([RigidBody])
        self.factory = factory
        self.friction = friction_ratio

    def update(self, sim: Simulator, dt: float, body: RigidBody) -> None:
        last_pos = body.pos

        body.pos, body.speed = self.next_state(body, dt)

        self.factory.board.update_pos(last_pos, body)

        body.speed *= self.friction * dt
        if np.linalg.norm(body.speed.data) < .5 * dt:
            body.speed *= 0

    @staticmethod
    def next_state(body: RigidBody, dt: float) -> Tuple[Vector, Vector]:
        next_speed = body.speed + body.accel * dt
        next_pos = body.pos + next_speed * dt
        return next_pos, next_speed
