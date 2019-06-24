from python_ecs.ecs import Component


class Background(Component):
    def __init__(self, r: int, g: int, b: int) -> None:
        super().__init__()
        self.color = (r, g, b)

    def __repr__(self):
        return 'Background({})'.format(self.color)
