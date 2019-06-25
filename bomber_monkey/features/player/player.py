from python_ecs.ecs import Component


class Player(Component):
    def __init__(self, no_player: int) -> None:
        super().__init__()
        self.no_player = no_player
