from typing import Tuple

from bomber_monkey.features.board.board import Board
from bomber_monkey.features.display.image import Image
from bomber_monkey.features.lifetime.lifetime import Lifetime
from bomber_monkey.features.move.position import Position
from bomber_monkey.features.move.speed import Speed
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.physics.shape import Shape
from python_ecs.ecs import sim


class BomberGameConfig(object):
    def __init__(self):
        self.tile_size = (64, 64)
        self.grid_size = (25, 15)
        self.bomb_timer_length = 3
        self.bomb_explosion_time = 1
        self.bomb_resizing_time = 1
        self.bomb_resizing_ratio = 0.1
        self.bomb_fire_time = 3

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

    def explode(self, x: float, y: float):
        return sim.create(
            Position(x, y),
            Shape(*self.tile_size),
            Image('resources/fire.png'),
            Lifetime(self.bomb_fire_time)
        )

    def board(self):
        return sim.create(Board(tile_size=self.tile_size, grid_size=self.grid_size))
