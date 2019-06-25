from bomber_monkey.features.board.board import Board, Tiles
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.physics.shape import Shape
from python_ecs.ecs import System, Entity


class WallCollisionSystem(System):
    def __init__(self, board: Entity):
        super().__init__([RigidBody, Shape])
        self.board: Board = board.get(Board)

    def update(self,
               body: RigidBody,
               shape: Shape) -> None:
        next_pos = body.pos + body.speed + body.accel
        cell = self.board.by_pixel(next_pos)
        if cell and cell.tile in (Tiles.BLOCK, Tiles.WALL):
            body.speed *= 0
            body.accel *= 0
