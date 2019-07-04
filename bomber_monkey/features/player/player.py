from bomber_monkey.features.player.player_slot import PlayerSlot
from python_ecs.ecs import Component


class Player(Component):
    def __init__(self, slot: PlayerSlot, power: int) -> None:
        super().__init__()
        self.power = power
        self.slot = slot

    @property
    def player_id(self):
        return self.slot.player_id

    @property
    def color(self):
        return self.slot.color
