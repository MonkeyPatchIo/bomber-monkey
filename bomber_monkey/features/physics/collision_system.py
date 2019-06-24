import math
from typing import Tuple

from bomber_monkey.features.board.board import Board, Tiles
from bomber_monkey.features.move.position import Position
from bomber_monkey.features.move.speed import Speed
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.physics.shape import Shape
from python_ecs.ecs import System, Entity


def direction(p0: Tuple[float, float], p1: Tuple[float, float]):
    return p1[0] - p0[0], p1[1] - p0[1]


class PlayerWallCollisionSystem(System):
    def __init__(self, board: Entity):
        super().__init__([Position, Speed, Shape, RigidBody])
        self.board = board.get(Board)  # type:Board

    def update(self,
               position: Position,
               speed: Speed,
               shape: Shape,
               body: RigidBody) -> None:
        next_pos = position.data + speed.data
        next_grid_pos = self.board.pixel_to_grid(next_pos)
        tile = self.board.get(*next_grid_pos.data)

        if tile in (Tiles.BLOCK, Tiles.WALL):
            speed.data *= 0
