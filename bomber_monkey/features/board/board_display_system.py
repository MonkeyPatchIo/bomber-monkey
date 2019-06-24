from typing import Tuple

from bomber_monkey.features.board.board import Board, Tiles
from bomber_monkey.features.display.image import Image
from bomber_monkey.features.move.position import Position
from python_ecs.ecs import System


class BoardDisplaySystem(System):
    def __init__(self, screen, tile_size: Tuple[int, int]):
        super().__init__([Board])
        self.screen = screen
        self.tile_size = tile_size
        self.images = {
            tile: Image('resources/tiles/{}.png'.format(str(tile).lower().replace('tiles.', '')))
            for tile in list(Tiles)
        }

    def update(self, board: Board) -> None:
        for x in range(board.width):
            for y in range(board.height):
                tile = board.get(x, y)
                image = self.images[tile]
                self.screen.blit(image.data, (x * self.tile_size[0], y * self.tile_size[1]))
