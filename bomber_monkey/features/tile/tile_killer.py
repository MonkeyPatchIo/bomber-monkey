from bomber_monkey.features.board.board import Tiles
from python_ecs.ecs import Component


class TileKiller(Component):
    def __init__(self, tile: Tiles) -> None:
        super().__init__()
        self.tile = tile
