from typing import Tuple

from bomber_monkey.features.board.board import Board, Tiles
from bomber_monkey.features.display.image import Image
from python_ecs.ecs import System


class BoardDisplaySystem(System):
    def __init__(self, screen, tile_size: Tuple[int, int]):
        super().__init__([Board])
        self.screen = screen
        self.tile_size = tile_size
        self.images = {
            tile: Image('resources/tiles/{}.png'.format(str(tile).lower().replace('tiles.', '')), tile_size)
            for tile in list(Tiles)
        }

    def update(self, board: Board) -> None:
        to_draw = [
            (
                self.images[board.get(x, y)].data,
                (x * self.tile_size[0], y * self.tile_size[1])
            )
            for x in range(board.width)
            for y in range(board.height)
        ]
        self.screen.blits(to_draw)
