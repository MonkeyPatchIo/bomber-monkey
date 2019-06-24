from python_ecs.ecs import Component


class Position(Component):
    def __init__(self, x: float, y: float) -> None:
        super().__init__()
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Position({},{})'.format(self.x, self.y)


