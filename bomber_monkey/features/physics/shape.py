from python_ecs.ecs import Component


class Shape(Component):
    def __init__(self, width: float, height: float) -> None:
        super().__init__()
        self.data = (width, height)

    @property
    def width(self):
        return self.data[0]

    @property
    def height(self):
        return self.data[1]

    def __repr__(self):
        return 'Shape({})'.format(self.data)
