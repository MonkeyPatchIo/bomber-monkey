from bomber_monkey.utils.image_loader import ImageLoader
from bomber_monkey.features.display.image import Image, Sprite

from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.physics.shape import Shape
from python_ecs.ecs import System, sim
import pygame as pg


class DisplaySystem(System):
    def __init__(self, image_loader: ImageLoader, screen):
        super().__init__([RigidBody, Image])
        self.image_loader = image_loader
        self.screen = screen
        self.images = {}

    def update(self, body: RigidBody, image: Image) -> None:
        entity = sim.get(body.eid)
        shape = entity.get(Shape)
        pos = body.pos
        if shape:
            pos = body.pos - shape.data // 2

        graphic = self.image_loader[image]
        self.screen.blit(pg.transform.scale(graphic, shape.data.data), pos.data)


class SpriteDisplaySystem(System):
    def __init__(self, image_loader: ImageLoader, screen):
        super().__init__([RigidBody, Sprite])
        self.image_loader = image_loader
        self.screen = screen
        self.images = {}

    def update(self, body: RigidBody, sprite: Sprite) -> None:
        entity = sim.get(body.eid)
        shape = entity.get(Shape)
        pos = body.pos
        if shape:
            pos = body.pos - shape.data // 2

        graphic = self.image_loader[sprite]
        image = graphic[sprite.current]

        if body.speed != [0, 0]:
            sprite.current = (sprite.current + 1) % sprite.anim_size
        else:
            sprite.current = 0

        self.screen.blit(pg.transform.scale(image, shape.data.data), pos.data)
