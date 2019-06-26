import time

from python_ecs.ecs import Component


class BombDropper(Component):
    def __init__(self, drop_rate: int) -> None:
        super().__init__()
        self.drop_rate = drop_rate
        self.last_drop = 0

    def drop(self) -> bool:
        now = time.time()
        if now - self.last_drop > self.drop_rate:
            self.last_drop = now
            return True

        return False


    def __repr__(self):
        return 'BombDropper({})'.format(self.drop_rate)