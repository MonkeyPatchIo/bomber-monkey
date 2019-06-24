import time

from bomber_monkey.bomber_game_config import BomberGameConfig
from bomber_monkey.features.bomb.bomb_explosion import BombExplosion
from bomber_monkey.features.lifetime.lifetime import Lifetime
from bomber_monkey.features.move.move import Position
from python_ecs.ecs import System, sim


class BombExplosionSystem(System):

    def __init__(self, conf: BomberGameConfig):
        super().__init__([BombExplosion, Position, Lifetime])
        self.conf = conf

    def update(self, explosion: BombExplosion, position: Position, lifetime: Lifetime) -> None:
        now = time.time()

        if not explosion.is_done and now > lifetime.dead_time:
            explosion.is_done = True
            sim.get(explosion.eid).destroy()
            for i in range(explosion.explosion_size):
                self.conf.create_explosion(position.data + (i * self.conf.tile_size.x, 0))
                self.conf.create_explosion(position.data - (i * self.conf.tile_size.x, 0))
                self.conf.create_explosion(position.data + (0, i * self.conf.tile_size.y))
                self.conf.create_explosion(position.data - (0, i * self.conf.tile_size.y))
