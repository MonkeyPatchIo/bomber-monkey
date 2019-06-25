import time
from typing import Tuple

from bomber_monkey.bomber_game_config import BomberGameConfig
from bomber_monkey.features.bomb.bomb_explosion import BombExplosion
from bomber_monkey.features.lifetime.lifetime import Lifetime
from bomber_monkey.features.physics.rigid_body import RigidBody
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
            for i in range(explosion.explosion_size):
                self._create_explosion(body, (i * self.conf.tile_size.x, 0))
                self._create_explosion(body, (-i * self.conf.tile_size.x, 0))
                self._create_explosion(body, (0, i * self.conf.tile_size.y))
                self._create_explosion(body, (0, - i * self.conf.tile_size.y))

    def _create_explosion(self, body: RigidBody, offset: Tuple[int, int]):
        self.conf.create_explosion(body.pos + offset)
