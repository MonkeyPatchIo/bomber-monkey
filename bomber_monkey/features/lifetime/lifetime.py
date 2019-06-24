import time

from python_ecs.ecs import Component


class Lifetime(Component):
    def __init__(self, lifetime: float) -> None:
        super().__init__()
        self.dead_time = time.time() + lifetime
