from typing import Tuple

from bomber_monkey.features.board.board import Board, Tiles
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.physics.shape import Shape
from python_ecs.ecs import System, Entity


def direction(p0: Tuple[float, float], p1: Tuple[float, float]):
    return p1[0] - p0[0], p1[1] - p0[1]


class PlayerWallCollisionSystem(System):
    def __init__(self, board: Entity):
        super().__init__([RigidBody, Shape])
        self.board: Board = board.get(Board)

    def update(self,
               body: RigidBody,
               shape: Shape) -> None:
        next_pos = body.pos + body.speed
        next_grid_pos = self.board.pixel_to_grid(next_pos)

        tile = self.board.get(*next_grid_pos.data)

        if tile in (Tiles.BLOCK, Tiles.WALL):
            body.speed *= 0
