import time

import pygame as pg

from bomber_monkey.features.banana.banana import Banana
from bomber_monkey.features.bomb.bomb import Bomb
from bomber_monkey.features.display.sprite import Sprite
from bomber_monkey.features.lifetime.lifetime import Lifetime
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.game_config import GameConfig
from python_ecs.ecs import System


class SpriteDisplaySystem(System):
    def __init__(self, conf: GameConfig, screen):
        super().__init__([RigidBody, Sprite])
        self.conf = conf
        self.image_loader = conf.image_loader
        self.screen = screen
        self.images = {}

    def update(self, dt: float, body: RigidBody, sprite: Sprite) -> None:
        entity = body.entity()
        bomb: Bomb = entity.get(Bomb)
        banana: Banana = entity.get(Banana)

        pos = body.pos
        if sprite.size:
            pos = body.pos - sprite.size // 2
        pos += self.conf.playground_offset

        graphic = self.image_loader[sprite]

        # FIXME: no specific code (Bomb, Banana) should stay here
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
        elif body.speed != [0, 0]:
            sprite.current = (sprite.current + 1) % sprite.anim_size
        else:
            sprite.current = 0
        image = graphic[sprite.current].copy()

        self.screen.blit(pg.transform.scale(image, sprite.size.data), pos.data)