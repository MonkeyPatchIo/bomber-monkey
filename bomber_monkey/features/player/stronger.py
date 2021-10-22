import time

from python_ecs.ecs import Component


class Stronger(Component):
    def __init__(self) -> None:
        super().__init__()
        self.time = 0
        self.start_time = time.time()
