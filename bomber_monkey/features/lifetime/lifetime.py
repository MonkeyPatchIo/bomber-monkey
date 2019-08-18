import sys

from python_ecs.ecs import Component


class Lifetime(Component):
    def __init__(self, time_to_live: float, delayed_ttl: bool = False) -> None:
        super().__init__()
        self.life_time = 0
        self.delayed_ttl = delayed_ttl
        self.time_to_live = time_to_live

    def time_to_live(self):
        if self.delayed_ttl:
            return sys.maxsize
        return self.time_to_live

    def is_ended(self):
        if self.delayed_ttl:
            return False
        return self.time_to_live <= 0

    def start_expiration(self):
        self.delayed_ttl = False

    def expire(self):
        self.time_to_live = 0

    def is_expiring(self):
        return not self.delayed_ttl

    def add_to_life(self, dt: float):
        if not self.delayed_ttl:
            self.time_to_live -= dt
        self.life_time += dt
