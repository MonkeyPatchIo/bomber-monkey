
from bomber_monkey.features.board.board import Board
from python_ecs.ecs import System, Simulator


class BoardSystem(System):
    def __init__(self):
        super().__init__([Board])

    def update(self, sim: Simulator, dt: float, board: Board) -> None:
        board.updates = []
