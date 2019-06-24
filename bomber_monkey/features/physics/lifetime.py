from python_ecs.ecs import Component

import datetime


class Lifetime(Component):
    def __init__(self, ttl: int) -> None:
        super().__init__()
        self.ttl = ttl
        self.start_time = datetime.datetime.now().timestamp()
