from bomber_monkey.utils.image_loader import ImageLoader
from bomber_monkey.features.board.board import Board, Tiles
from bomber_monkey.features.display.image import Image
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import System


class BoardDisplaySystem(System):
    def __init__(self, image_loader: ImageLoader, screen, tile_size: Vector):
        super().__init__([Board])
        self.image_loader = image_loader
        self.last_update = -1
        self.screen = screen
        self.empty = None
        self.buffer = screen.copy()
        self.tile_size = tile_size
        self.images = {
            tile: Image('resources/tiles/{}.png'.format(str(tile).lower().replace('tiles.', '')), tile_size)
            for tile in list(Tiles)
        }
        self.empty_special = Image('resources/tiles/empty_up.png', tile_size)

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
        top = cell.up()
        if top is not None and cell.tile is Tiles.EMPTY and top.tile is Tiles.WALL:
            return self.empty_special
        return self.images[tile]
