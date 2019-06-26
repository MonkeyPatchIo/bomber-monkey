from bomber_monkey.utils.image_loader import ImageLoader
from bomber_monkey.features.board.board import Board, Tiles
from bomber_monkey.features.display.image import Image
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import System


class BoardDisplaySystem(System):
    def __init__(self, image_loader: ImageLoader, screen, tile_size: Vector, tile_set: str = 'jungle'):
        super().__init__([Board])
        self.tile_set = tile_set
        self.image_loader = image_loader
        self.last_update = -1
        self.screen = screen
        self.empty = None
        self.buffer = screen.copy()
        self.tile_size = tile_size
        self.images = {
            tile: Image(
                'resources/tiles/{}_{}.png'.format(
                    self.tile_set,
                    str(tile).lower().replace('tiles.', '')),
                tile_size)
            for tile in list(Tiles)
        }

    def update(self, board: Board) -> None:
        if board.last_update > self.last_update:
            self.last_update = board.last_update
            if not self.empty:
                self.empty = self.screen.copy()
                for x in range(board.width):
                    for y in range(board.height):
                        self.empty.blit(
                            self.image_loader[self.images[Tiles.EMPTY]],
                            (x * self.tile_size.x, y * self.tile_size.y)
                        )
            self.buffer.blit(self.empty, (0, 0))
            for x in range(board.width):
                for y in range(board.height):
                    self.buffer.blit(
                        self.image_loader[self._image(board, x, y)],
                        (x * self.tile_size.x, y * self.tile_size.y)
                    )
        self.screen.blit(self.buffer, (0, 0))

    def _image(self, board: Board, x: int, y: int) -> Image:
        cell = board.by_grid(Vector.create(x, y))
        tile = cell.tile
        return self.images[tile]
