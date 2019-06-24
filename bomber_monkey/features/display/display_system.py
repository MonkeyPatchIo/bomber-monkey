from bomber_monkey.features.display.image import Image
from bomber_monkey.features.move.position import Position
from python_ecs.ecs import System


class DisplaySystem(System):
    def __init__(self, screen):
        super().__init__([Position, Image])
        self.screen = screen

    def update(self, position: Position, image: Image) -> None:
        self.screen.blit(image.data, (position.x, position.y))
