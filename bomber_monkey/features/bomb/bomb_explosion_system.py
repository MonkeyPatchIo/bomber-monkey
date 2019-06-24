from bomber_monkey.bomber_game_config import BomberGameConfig
from bomber_monkey.features.bomb.bomb_explosion import BombExplosion
from bomber_monkey.features.display.image import Image
from bomber_monkey.features.move.position import Position
from bomber_monkey.features.physics.shape import Shape
from bomber_monkey.features.physics.lifetime import Lifetime
from python_ecs.ecs import System, ECS
import datetime
import math


class BombExplosionSystem(System):

    def __init__(self, sim: ECS, conf: BomberGameConfig):
        super().__init__([BombExplosion, Position, Shape])
        self.sim = sim
        self.conf = conf

    def update(self, explosion: BombExplosion, position: Position, shape: Shape) -> None:
        age = datetime.datetime.now().timestamp() - explosion.start_time
        if age > self.conf.bomb_timer_length + self.conf.bomb_explosion_time:
            self.sim.get(explosion.eid).destroy()
        elif age > self.conf.bomb_timer_length:
            for i in range(explosion.explosion_size):
                self.sim.create(
                    Position(position.x + i * self.conf.tile_size[0], position.y),
                    Shape(*self.conf.tile_size),
                    Image('resources/fire.png'),
                    Lifetime(self.conf.bomb_fire_time)
                )
                self.sim.create(
                    Position(position.x - i * self.conf.tile_size[0], position.y),
                    Shape(*self.conf.tile_size),
                    Image('resources/fire.png'),
                    Lifetime(self.conf.bomb_fire_time)
                )
                self.sim.create(
                    Position(position.x, position.y + i * self.conf.tile_size[1]),
                    Shape(*self.conf.tile_size),
                    Image('resources/fire.png'),
                    Lifetime(self.conf.bomb_fire_time)
                )
                self.sim.create(
                    Position(position.x, position.y - i * self.conf.tile_size[1]),
                    Shape(*self.conf.tile_size),
                    Image('resources/fire.png'),
                    Lifetime(self.conf.bomb_fire_time)
                )
        else:
            ratio = math.cos(age / self.conf.bomb_resizing_time * 2 * math.pi) * self.conf.bomb_resizing_ratio
            #shape.width = ratio * explosion.initial_size[0]
            #shape.height = ratio * explosion.initial_size[1]
