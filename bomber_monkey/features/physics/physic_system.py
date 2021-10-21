from typing import Tuple

import numpy as np

from bomber_monkey.features.board.board import Board
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.game_config import GameConfig
from bomber_monkey.utils.vector import Vector, sign
from python_ecs.ecs import System, Simulator


class PlayerCollisionPhysic:

    def update(self, sim: Simulator, dt: float, body: RigidBody, next_pos: Vector, next_speed: Vector) -> Tuple[Vector, Vector]:
        raise NotImplementedError()


def check_pos_diff(last_pos: Vector, new_pos: Vector, max_pos_diff: Vector):
    diff = new_pos - last_pos
    if abs(diff.x) > max_pos_diff.x:
        new_pos.x = last_pos.x + sign(diff.x) * max_pos_diff.x
    if abs(diff.y) > max_pos_diff.y:
        new_pos.y = last_pos.y + sign(diff.y) * max_pos_diff.y
    return new_pos


class PhysicSystem(System):
    def __init__(self, collision_physic: PlayerCollisionPhysic):
        super().__init__([RigidBody])
        self.collision_physic = collision_physic

    def update(self, sim: Simulator, dt: float, body: RigidBody) -> None:
        conf: GameConfig = sim.context.conf
        board: Board = sim.context.board

        max_speed = body.max_speed if body.max_speed is not None else conf.player_max_speed

        next_speed = body.accel * dt + body.speed
        next_speed.x = max(min(next_speed.x, max_speed), -max_speed)
        next_speed.y = max(min(next_speed.y, max_speed), -max_speed)
        next_pos = body.accel * 0.5 * dt * dt + body.speed * dt + body.pos

        next_pos = check_pos_diff(body.pos, next_pos, conf.max_pos_diff)

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

        board.update_pos(last_pos, body)
