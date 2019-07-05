import time

import pygame as pg

from bomber_monkey.features.banana.banana import Banana
from bomber_monkey.features.bomb.bomb import Bomb
from bomber_monkey.features.display.image import Image, Sprite
from bomber_monkey.features.lifetime.lifetime import Lifetime
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.physics.shape import Shape
from bomber_monkey.features.player.player import Player
from bomber_monkey.game_config import GameConfig
from python_ecs.ecs import System


class DisplaySystem(System):
    def __init__(self, conf: GameConfig, screen):
        super().__init__([RigidBody, Image])
        self.conf = conf
        self.image_loader = self.conf.image_loader
        self.screen = screen
        self.images = {}

    def update(self, dt: float, body: RigidBody, image: Image) -> None:
        shape = body.shape
        pos = body.pos
        if shape:
            pos = body.pos - shape.data // 2
        pos += self.conf.playground_offset

        graphic = self.image_loader[image]
        self.screen.blit(pg.transform.scale(graphic, shape.data.data), pos.data)


class SpriteDisplaySystem(System):
    def __init__(self, conf: GameConfig, screen):
        super().__init__([RigidBody, Sprite])
        self.conf = conf
        self.image_loader = conf.image_loader
        self.screen = screen
        self.images = {}

    def update(self, dt: float, body: RigidBody, sprite: Sprite) -> None:
        entity = body.entity()
        shape = body.shape
        bomb: Bomb = entity.get(Bomb)
        banana: Banana = entity.get(Banana)
        player: Player = entity.get(Player)

        pos = body.pos
        if shape:
            pos = body.pos - shape.data // 2
        pos += self.conf.playground_offset

        graphic = self.image_loader[sprite]

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

        if player:
            w, h = image.get_size()
            for x in range(w):
                for y in range(h):
                    color = image.get_at((x, y))
                    player_color = pg.Color(*player.color)
                    player_color.r = player_color.r // 5
                    player_color.g = player_color.g // 5
                    player_color.b = player_color.b // 5

                    if color[3] > 0:
                        final_color = color + player_color
                    else:
                        final_color = color
                    image.set_at((x, y), final_color)

        self.screen.blit(pg.transform.scale(image, shape.data.data), pos.data)
