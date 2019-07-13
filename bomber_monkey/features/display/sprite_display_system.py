import time

import numpy as np
import pygame as pg
from pygame.rect import Rect

from bomber_monkey.features.banana.banana import Banana
from bomber_monkey.features.bomb.bomb import Bomb
from bomber_monkey.features.bomb.explosion import Explosion, ExplosionDirection
from bomber_monkey.features.display.sprite import Sprite
from bomber_monkey.features.lifetime.lifetime import Lifetime
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.game_config import GameConfig
from python_ecs.ecs import System, Simulator

EPSILON = 0.1


class SpriteDisplaySystem(System):
    def __init__(self, conf: GameConfig, screen):
        super().__init__([RigidBody, Sprite])
        self.conf = conf
        self.image_loader = conf.image_loader
        self.screen = screen
        self.images = {}

    def update(self, sim: Simulator, dt: float, body: RigidBody, sprite: Sprite) -> None:
        conf: GameConfig = sim.context.conf

        entity = body.entity()
        bomb: Bomb = entity.get(Bomb)
        banana: Banana = entity.get(Banana)
        explosion: Explosion = entity.get(Explosion)

        pos = body.pos
        if sprite.size:
            pos = body.pos - sprite.size // 2
        if sprite.offset:
            pos += sprite.offset
        pos += self.conf.playground_offset

        graphic = self.image_loader[sprite]

        # FIXME: no specific code (Bomb, Banana) should stay here
        rotate = None
        if bomb:
            lifetime: Lifetime = entity.get(Lifetime)
            now = time.time()
            time_to_live = max(lifetime.dead_time - now, 0)
            anim = (sprite.anim_size - 1) * (1 - time_to_live / lifetime.duration)
            sprite.current = int(anim)
        elif banana:
            now = time.time()
            anim_time = sprite.anim_time
            ratio = (now % anim_time) / anim_time
            sprite.current = int(ratio * sprite.anim_size)
        elif explosion:
            now = time.time()
            current = int((now - explosion.start_time) / sprite.anim_time)
            if current < 0:
                return
            if current >= sprite.anim_size:
                current = sprite.anim_size - 2 + ((current - sprite.anim_size) % 2)
            if explosion.direction == ExplosionDirection.LEFT:
                rotate = 90
            elif explosion.direction == ExplosionDirection.DOWN:
                rotate = 180
            elif explosion.direction == ExplosionDirection.RIGHT:
                rotate = -90
            sprite.current = current
        elif np.linalg.norm(body.speed.data) > EPSILON:
            sprite.current = (sprite.current + 1) % sprite.anim_size
        else:
            sprite.current = 0
        image = graphic[sprite.current].copy()

        if rotate is not None:
            image = pg.transform.rotate(image, rotate)
        self.screen.blit(pg.transform.scale(image, sprite.size.data), pos.data)

        if conf.DEBUG_MODE and body.shape:
            shape_pos = body.pos - body.shape.data // 2 + self.conf.playground_offset
            pg.draw.rect(self.screen, (10, 50, 100), Rect(shape_pos.as_ints(), (body.shape.width, body.shape.height)), 1)
