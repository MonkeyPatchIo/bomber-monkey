import pygame as pg
from pygame.rect import Rect

from bomber_monkey.features.display.sprite import Sprite
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.game_config import GameConfig
from python_ecs.ecs import System, Simulator

EPSILON = 0.1


class SpriteDisplaySystem(System):
    def __init__(self, conf: GameConfig, screen):
        super().__init__([RigidBody, Sprite])
        self.conf = conf
        self.graphics_cache = conf.graphics_cache
        self.screen = screen
        self.images = {}

    def update(self, sim: Simulator, dt: float, body: RigidBody, sprite: Sprite) -> None:
        conf: GameConfig = sim.context.conf

        pos = body.pos - sprite.display_size // 2
        if sprite.offset is not None:
            pos += sprite.offset
        pos += self.conf.playground_offset

        graphic = self.graphics_cache.get_sprite(sprite)

        transformation = sprite.animation.next(body, sprite.animation_data)

        sprite.animation_data.current_image_index = transformation.sprite_index
        image = graphic[transformation.sprite_index].copy()

        if transformation.rotation != 0:
            image = pg.transform.rotate(image, transformation.rotation)
        if transformation.vertical_flip:
            image = pg.transform.flip(image, True, False)
        self.screen.blit(pg.transform.scale(image, sprite.display_size.data), pos.data)

        if conf.DEBUG_MODE and body.shape:
            shape_pos = body.pos - body.shape.data // 2 + self.conf.playground_offset
            pg.draw.rect(self.screen, (10, 50, 100), Rect(shape_pos.as_ints(), (body.shape.width, body.shape.height)), 1)
