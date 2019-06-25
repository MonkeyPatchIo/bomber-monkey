from bomber_monkey.features.display.image import Image

from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.physics.shape import Shape
from python_ecs.ecs import System, sim
import pygame as pg


class DisplaySystem(System):
    def __init__(self, screen):
        super().__init__([RigidBody, Image])
        self.screen = screen

    def update(self, body: RigidBody, image: Image) -> None:
        entity = sim.get(body.eid)
        shape = entity.get(Shape)
        pos = body.pos
        if shape:
            pos = body.pos - shape.data // 2
        self.screen.blit(pg.transform.scale(image.data, shape.data.data), pos.data)
