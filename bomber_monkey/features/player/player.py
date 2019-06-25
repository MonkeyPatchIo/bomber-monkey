from python_ecs.ecs import Component


class Player(Component):
    def __init__(self, player_id: int) -> None:
        super().__init__()
        self.player_id = player_id
