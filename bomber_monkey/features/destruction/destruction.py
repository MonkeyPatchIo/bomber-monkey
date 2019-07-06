from python_ecs.ecs import Component


class Destruction(Component):
    def __init__(self) -> None:
        super().__init__()


class Protection(Component):
    def __init__(self, duration: float) -> None:
        super().__init__()
        self.remaining = duration
