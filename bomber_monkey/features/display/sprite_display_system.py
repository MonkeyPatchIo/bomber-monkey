import time
import pygame as pg
from pygame.rect import Rect

from bomber_monkey.features.display.sprite import Sprite, SpriteSet
from bomber_monkey.features.display.sprite_animation import merge_transformation_custom_data
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.game_config import GameConfig
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import System, Simulator

EPSILON = 0.1


def draw_sprite(sim: Simulator, screen, sprite: Sprite, body: RigidBody):
    if not sprite.display:
        return

    conf: GameConfig = sim.context.conf

    pos = body.pos - sprite.display_size // 2
    pos += conf.playground_offset

    graphic = conf.graphics_cache.get_sprite(sprite)

    now = time.time()
    transformation = sprite.animation.animate(body, now, sprite.animation_data)

    sprite.animation_data.current_image_index = transformation.sprite_index
    sprite.animation_data.custom_data = merge_transformation_custom_data(transformation, sprite.animation_data)
    image = graphic[transformation.sprite_index].copy()

    if transformation.rotation != 0:
        image = pg.transform.rotate(image, transformation.rotation)
    if transformation.vertical_flip:
        image = pg.transform.flip(image, True, False)
    if transformation.translation is not None:
        pos += transformation.translation

    if sprite.offset is not None:
        if transformation.vertical_flip:
            pos += Vector.create(-sprite.offset.x, sprite.offset.y)
        else:
            pos += sprite.offset

    screen.blit(pg.transform.scale(image, sprite.display_size.data), pos.data)

    if conf.DEBUG_MODE and body.shape:
        shape_pos = body.pos - body.shape.data // 2 + conf.playground_offset
        pg.draw.rect(screen, (10, 50, 100), Rect(shape_pos.as_ints(), (body.shape.width, body.shape.height)), 1)


class SpriteDisplaySystem(System):
    def __init__(self, conf: GameConfig, screen, layer: int = 0):
        super().__init__([RigidBody, Sprite])
        self.conf = conf
        self.graphics_cache = conf.graphics_cache
        self.screen = screen
        self.layer = layer

    def update(self, sim: Simulator, dt: float, body: RigidBody, sprite: Sprite) -> None:
        if sprite.layer != self.layer:
            return
        draw_sprite(sim, self.screen, sprite, body)


class SpriteSetDisplaySystem(System):
    def __init__(self, conf: GameConfig, screen, layer: int = 0):
        super().__init__([RigidBody, SpriteSet])
        self.conf = conf
        self.graphics_cache = conf.graphics_cache
        self.screen = screen
        self.layer = layer

    def update(self, sim: Simulator, dt: float, body: RigidBody, sprite_set: SpriteSet) -> None:
        for sprite in sprite_set.sprites:
            if sprite.layer == self.layer:
                draw_sprite(sim, self.screen, sprite, body)
