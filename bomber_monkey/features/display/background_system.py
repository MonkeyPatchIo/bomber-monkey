from bomber_monkey.features.display.background import Background
from python_ecs.ecs import System


class BackgroundSystem(System):
    def __init__(self, screen):
        super().__init__([Background])
        self.screen = screen

    def update(self, bgd: Background) -> None:
        self.screen.fill(bgd.color)
