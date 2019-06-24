from python_ecs.ecs import Component

import datetime


class BombExplosion(Component):
    def __init__(self, conf, explosion_size) -> None:
        super().__init__()
        self.initial_size = conf.tile_size
        self.explosion_size = explosion_size
        self.start_time = datetime.datetime.now().timestamp()

    def __repr__(self):
        return 'BombExplosion()'
