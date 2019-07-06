import pygame as pg

from bomber_monkey.features.display.image import Image
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.game_config import GameConfig
from python_ecs.ecs import System


class ImageDisplaySystem(System):
    def __init__(self, conf: GameConfig, screen):
        super().__init__([RigidBody, Image])
        self.conf = conf
        self.image_loader = self.conf.image_loader
        self.screen = screen
        self.images = {}

    def update(self, dt: float, body: RigidBody, image: Image) -> None:
        pos = body.pos
        if image.size:
            pos = body.pos - image.size // 2
        pos += self.conf.playground_offset

        graphic = self.image_loader[image]
        self.screen.blit(pg.transform.scale(graphic, image.size.data), pos.data)
