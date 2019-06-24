import pygame

from python_ecs.ecs import Component


class Image(Component):
    def __init__(self, path: str) -> None:
        super().__init__()
        self.path = path
        self.data = pygame.image.load(path)

    def __repr__(self):
        return 'Image({})'.format(self.path)


