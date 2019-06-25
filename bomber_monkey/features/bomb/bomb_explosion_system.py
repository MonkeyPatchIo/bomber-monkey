import time
from typing import Tuple

from bomber_monkey.bomber_game_config import BomberGameConfig
from bomber_monkey.features.board.board import Tiles, Cell
from bomber_monkey.features.bomb.bomb_explosion import BombExplosion
from bomber_monkey.features.lifetime.lifetime import Lifetime
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import System, sim


class BombExplosionSystem(System):

    def __init__(self, conf: BomberGameConfig):
        super().__init__([BombExplosion, RigidBody, Lifetime])
        self.conf = conf

    def update(self, explosion: BombExplosion, body: RigidBody, lifetime: Lifetime) -> None:
        now = time.time()

        if not explosion.is_done and now > lifetime.dead_time:
            explosion.is_done = True
            sim.get(explosion.eid).destroy()
            bomb_cell: Cell = self.conf.board.by_pixel(body.pos)
            self.conf.create_explosion(bomb_cell.center)
            directions = [Vector.create(x, y) for x, y in [(0, -1), (1, 0), (0, 1), (-1, 0)]]
            for direction in directions:
                for i in range(1, explosion.explosion_size + 1):
                    cell: Cell = bomb_cell.move(direction * i)
                    if cell is None or cell.tile == Tiles.WALL:
                        break
                    self.conf.create_explosion(cell.center)
                    if cell.tile == Tiles.TREE0:
                        cell.tile = Tiles.EMPTY
                        break
