import sys
import time

from python_ecs.ecs import Component


class Lifetime(Component):
    def __init__(self, duration: float, delayed: bool = False) -> None:
        super().__init__()
        self.dead_time = time.time() + duration if not delayed else None
        self.duration = duration

    def time_to_live(self):
        if self.dead_time is None:
            return sys.maxsize
        return time.time() - self.dead_time

    def is_ended(self):
        if self.dead_time is None:
            return False
        return self.dead_time < time.time()

    def start_expiration(self):
        if self.dead_time is None:
            self.dead_time = time.time() + self.duration

    def expire(self):
        self.dead_time = 0

    def is_expiring(self):
        return self.dead_time is not None
