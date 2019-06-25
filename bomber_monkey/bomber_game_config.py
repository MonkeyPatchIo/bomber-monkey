import time

from bomber_monkey.features.board.board import Board, random_blocks, Tiles, fill_border, clear_corners
from bomber_monkey.features.bomb.bomb_explosion import BombExplosion
from bomber_monkey.features.display.image import Image
from bomber_monkey.features.lifetime.lifetime import Lifetime
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.physics.shape import Shape
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import sim, Entity


class BomberGameConfig(object):
    def __init__(self):
        self.grid_size = Vector.create(20, 12)
        self.tile_size = Vector.create(64, 64)
        self.bomb_duration = 2.5
        self.bomb_resizing_time = 1
        self.bomb_resizing_ratio = 0.1
        self.explosion_duration = .2
        self._board: Board = None

    @property
    def pixel_size(self) -> Vector:
        return self.tile_size.data * self.grid_size.data

    def create_player(self, grid_pos: Vector):
        pos = grid_pos * self.tile_size + self.tile_size // 2

        return sim.create(
            RigidBody(
                pos=pos
            ),
            Shape(self.tile_size),
            Image('resources/monkey.png')
        )

    def create_explosion(self, pos: Vector):
        return sim.create(
            RigidBody(pos=pos),
            Shape(self.tile_size),
            Image('resources/fire.png'),
            Lifetime(self.explosion_duration)
        )

    def create_board(self):
        if self.board:
            raise ValueError('board is already created')

        board = Board(tile_size=self.tile_size, grid_size=self.grid_size)
        random_blocks(board, Tiles.WALL, .2)
        random_blocks(board, Tiles.BLOCK, .5)
        clear_corners(board)
        fill_border(board, Tiles.WALL)
        self._board = board

        return sim.create(board)

    @property
    def board(self) -> Board:
        return self._board

    def create_bomb(self, avatar: Entity):
        global last_creation
        now = time.time()
        if now - last_creation > .5:
            last_creation = now
            board: Board = self.board
            body: RigidBody = avatar.get(RigidBody)

            bomb_pos = board.by_pixel(body.pos).center
            sim.create(
                RigidBody(
                    pos=bomb_pos
                ),
                Shape(self.tile_size),
                Image('resources/bomb.png'),
                Lifetime(self.bomb_duration),
                BombExplosion(3)
            )


last_creation = time.time()
