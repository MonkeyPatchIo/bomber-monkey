from python_ecs.ecs import Component


class Player(Component):
    def __init__(self, player_id: int, power: int) -> None:
        super().__init__()
        self.power = power
        self.player_id = player_id
