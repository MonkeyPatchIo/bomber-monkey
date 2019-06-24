from python_ecs.ecs import Component

import datetime


class Lifetime(Component):
    def __init__(self, lifetime: int) -> None:
        super().__init__()
        self.dead_time = datetime.datetime.now().timestamp() + lifetime
