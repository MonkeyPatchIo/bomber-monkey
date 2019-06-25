from bomber_monkey.features.board.board import Board, Tiles
from bomber_monkey.features.display.image import Image
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import System


class BoardDisplaySystem(System):
    def __init__(self, screen, tile_size: Vector):
        super().__init__([Board])
        self.last_update = -1
        self.screen = screen
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
            for x in range(board.width):
                for y in range(board.height):
                    self.buffer.blit(
                        self._image(board, x, y).data,
                        (x * self.tile_size.x, y * self.tile_size.y)
                    )
        self.screen.blit(self.buffer, (0, 0))

    def _image(self, board: Board, x: int, y: int) -> Image:
        tile = board.by_grid(Vector.create(x, y)).tile
        if y > 0 and tile is Tiles.EMPTY and board.by_grid(Vector.create(x, y - 1)).tile is not Tiles.EMPTY:
            return self.empty_special
        return self.images[tile]
