from bomber_monkey.features.display.image import Image
from bomber_monkey.features.move.move import Position
from bomber_monkey.features.physics.shape import Shape
from python_ecs.ecs import System, sim
import pygame as pg


class DisplaySystem(System):
    def __init__(self, screen):
        super().__init__([Position, Image])
        self.screen = screen

    def update(self, position: Position, image: Image) -> None:
        entity = sim.get(position.eid)
        shape = entity.get(Shape)
        pos = position.data
        if shape:
            pos -= shape.data // 2
        self.screen.blit(pg.transform.scale(image.data, shape.data.data), pos.data)
