from python_ecs.ecs import Component


class Banana(Component):
    def __init__(self) -> None:
        super().__init__()

    def __repr__(self):
        return 'Banana()'
