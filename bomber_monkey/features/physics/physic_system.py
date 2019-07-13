from typing import Tuple

import numpy as np

from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.game_config import GameConfig
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import System, Simulator


class PlayerCollisionPhysic:

    def update(self, sim: Simulator, dt: float, body: RigidBody, next_pos: Vector, next_speed: Vector) -> Tuple[Vector, Vector]:
        raise NotImplementedError()


class PhysicSystem(System):
    def __init__(self, collision_physic: PlayerCollisionPhysic):
        super().__init__([RigidBody])
        self.collision_physic = collision_physic

    def update(self, sim: Simulator, dt: float, body: RigidBody) -> None:
        conf: GameConfig = sim.context.conf

        next_speed = body.accel * dt + body.speed
        next_speed.x = max(min(next_speed.x, conf.player_max_speed), -conf.player_max_speed)
        next_speed.y = max(min(next_speed.y, conf.player_max_speed), -conf.player_max_speed)
        next_pos = body.accel * 0.5 * dt * dt + body.speed * dt + body.pos

        if body.accel.x == 0:
            next_speed.x *= conf.friction_ratio
        if body.accel.y == 0:
            next_speed.y *= conf.friction_ratio
        if np.linalg.norm(next_speed.data) < 10:
            next_speed *= 0

        next_pos, next_speed = self.collision_physic.update(sim, dt, body, next_pos, next_speed)

        last_pos = body.pos

        body.accel = Vector.create()
        body.speed = next_speed
        body.pos = next_pos

        sim.context.board.update_pos(last_pos, body)

