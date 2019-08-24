from typing import Tuple

from bomber_monkey.utils.vector import Vector


class PlayerSlot(object):
    def __init__(self,
                 player_id: int,
                 start_pos: Vector,
                 color: Tuple[int, int, int]):
        self.player_id = player_id
        self.start_pos = start_pos
        self.color = color
