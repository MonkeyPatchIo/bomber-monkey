from bomber_monkey.features.board.board import Board, Tiles
from bomber_monkey.features.display.image import Image
from bomber_monkey.features.display.sprite import Sprite
from bomber_monkey.features.player.player import Player
from bomber_monkey.game_config import GameConfig
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import System, Simulator


class BoardDisplaySystem(System):
    def __init__(self, conf: GameConfig, screen, tile_set: str = 'jungle'):
        super().__init__([Board])
        self.conf = conf
        self.tile_set = tile_set
        self.graphics_cache = conf.graphics_cache
        self.last_update = -1
        self.screen = screen
        self.empty = None
        self.buffer = screen.copy()
        self.tile_size = conf.tile_size
        self.images = {
            tile: Image(
                self.conf.media_path('tiles/{}_{}.png'.format(
                    self.tile_set,
                    str(tile).lower().replace('tiles.', ''))),
                conf.tile_size)
            for tile in list(Tiles)
        }

    def update(self, sim: Simulator, dt: float, board: Board) -> None:
        if board.last_update > self.last_update:
            self.last_update = board.last_update
            if not self.empty:
                self.empty = self.screen.copy()
                for x in range(board.width):
                    for y in range(board.height):
                        self.empty.blit(self.graphics_cache.get_image(self.images[Tiles.EMPTY]), self._pos(x, y))
            self.buffer.blit(self.empty, (0, 0))
            for x in range(board.width):
                for y in range(board.height):
                    self.buffer.blit(self.graphics_cache.get_image(self._image(board, x, y)), self._pos(x, y))

        # display game
        self.screen.blit(self.buffer, (0, 0))

        if self.conf.DEBUG_MODE:
            for x in range(board.width):
                for y in range(board.height):
                    cell = board.by_grid(Vector.create(x, y))
                    for p in cell.get(Player):
                        sprite: Sprite = p.get(Sprite)
                        self.screen.blit(self.graphics_cache.get_sprite(sprite)[0], self._pos(x, y))

    def _pos(self, x, y):
        return x * self.tile_size.x + self.conf.playground_offset.x, y * self.tile_size.y + self.conf.playground_offset.y

    def _image(self, board: Board, x: int, y: int) -> Image:
        cell = board.by_grid(Vector.create(x, y))
        tile = cell.tile
        return self.images[tile]
