from typing import List

from bomber_monkey.features.board.board import Cell
from python_ecs.ecs import Component


class Collision(Component):
    def __init__(self,
                 cells: List[Cell]
                 ) -> None:
        super().__init__()
        self.cells = cells

    def __repr__(self):
        return 'Collision({})'.format(self.cells)

