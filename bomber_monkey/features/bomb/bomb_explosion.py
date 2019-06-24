from python_ecs.ecs import Component


class BombExplosion(Component):
    def __init__(self, explosion_size: int) -> None:
        super().__init__()
        self.explosion_size = explosion_size
        self.is_done = False

    def __repr__(self):
        return 'BombExplosion({})'.format(self.explosion_size)
