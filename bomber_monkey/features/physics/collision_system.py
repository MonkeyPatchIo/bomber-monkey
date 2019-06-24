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
        grid_pos = self.board.pixel_to_grid(position.data)
        tile = self.board.get(*grid_pos)

        if tile in (Tiles.BLOCK, Tiles.WALL):
            position.x -= speed.x
            position.y -= speed.y
            speed.data = (0, 0)
