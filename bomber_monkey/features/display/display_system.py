from bomber_monkey.features.display.image import Image
from bomber_monkey.features.move.position import Position
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
        x, y = position.data
        if shape:
            x -= shape.width // 2
            y -= shape.height // 2
        self.screen.blit(pg.transform.scale(image.data, shape.data), (x, y))
