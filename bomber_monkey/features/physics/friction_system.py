from bomber_monkey.features.move.move import Speed
from python_ecs.ecs import System


class FrictionSystem(System):
    def __init__(self, ratio: float):
        super().__init__([Speed])
        self.ratio = ratio

    def update(self, speed: Speed) -> None:
        speed.data *= self.ratio
