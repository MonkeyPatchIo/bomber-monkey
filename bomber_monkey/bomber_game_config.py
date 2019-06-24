from typing import Tuple

from bomber_monkey.features.board.board import Board
from bomber_monkey.features.display.image import Image
from bomber_monkey.features.move.position import Position
from bomber_monkey.features.move.speed import Speed
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.physics.shape import Shape
from python_ecs.ecs import sim


class BomberGameConfig(object):
    def __init__(self):
        self.tile_size = (64, 64)
        self.grid_size = (25, 15)

    @property
    def grid_pixel_size(self) -> Tuple[int, int]:
        return self.tile_size[0] * self.grid_size[0], self.tile_size[1] * self.grid_size[1]

    def player(self, grid_x: int, grid_y: int):
        return sim.create(
            Position(
                grid_x * self.tile_size[0] + self.tile_size[0] // 2,
                grid_y * self.tile_size[1] + self.tile_size[1] // 2
            ),
            Speed(),
            Shape(*self.tile_size),
            RigidBody(),
            Image('resources/monkey.png')
        )

    def board(self):
        return sim.create(Board(tile_size=self.tile_size, grid_size=self.grid_size))
