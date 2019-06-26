from python_ecs.ecs import Component


class Bomb(Component):
    def __init__(self, explosion_size: int) -> None:
        super().__init__()
        self.explosion_size = explosion_size
        self.has_explode = False

    def __repr__(self):
        return 'Bomb({})'.format(self.explosion_size)
