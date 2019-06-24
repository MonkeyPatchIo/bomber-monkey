from python_ecs.ecs import Component


class Speed(Component):
    def __init__(self, x: float=0, y: float=0) -> None:
        super().__init__()
        self.data = (x, y)

    @property
    def x(self):
        return self.data[0]

    @x.setter
    def x(self, x: float):
        self.data = (x, self.y)

    @property
    def y(self):
        return self.data[1]

    @y.setter
    def y(self, y: float):
        self.data = (self.x, y)

    def __repr__(self):
        return 'Speed({})'.format(self.data)
