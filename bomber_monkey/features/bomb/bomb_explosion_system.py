import datetime

from bomber_monkey.bomber_game_config import BomberGameConfig
from bomber_monkey.features.bomb.bomb_explosion import BombExplosion
from bomber_monkey.features.lifetime.lifetime import Lifetime
from bomber_monkey.features.move.position import Position
from bomber_monkey.features.physics.shape import Shape
from python_ecs.ecs import System, sim


class BombExplosionSystem(System):

    def __init__(self, conf: BomberGameConfig):
        super().__init__([BombExplosion, Position, Lifetime, Shape])
        self.conf = conf

    def update(self, explosion: BombExplosion, position: Position, lifetime: Lifetime, shape: Shape) -> None:
        now = datetime.datetime.now().timestamp()

        if not explosion.is_done and now > lifetime.dead_time:
            explosion.is_done = True
            sim.get(explosion.eid).destroy()
            for i in range(explosion.explosion_size):
                self.conf.explode(position.x + i * self.conf.tile_size[0], position.y)
                self.conf.explode(position.x - i * self.conf.tile_size[0], position.y)
                self.conf.explode(position.x, position.y + i * self.conf.tile_size[1])
                self.conf.explode(position.x, position.y - i * self.conf.tile_size[1])
