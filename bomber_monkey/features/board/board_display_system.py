import time

from pygame.surface import Surface

from bomber_monkey.features.board.board import Board, Tiles, TileEffect
from bomber_monkey.features.display.image import Image
from bomber_monkey.features.display.sprite import Sprite
from bomber_monkey.features.player.player import Player
from bomber_monkey.game_config import GameConfig
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import System, Simulator

TILE_SHAKE_DURATION = 0.8
TILE_SHAKE_SIZE = 5


class TileSet:
    def __init__(self, conf: GameConfig, tile_set_name: str = 'jungle'):
        self.images = {
            tile: Image(
                conf.media_path('tiles/{}_{}.png'.format(
                    tile_set_name,
                    str(tile).lower().replace('tiles.', ''))),
                conf.tile_size)
            for tile in list(Tiles)
        }


class BoardDisplaySystem(System):
    def __init__(self, conf: GameConfig, screen):
        super().__init__([Board])
        self.conf = conf
        self.tile_set = TileSet(conf)
        self.graphics_cache = conf.graphics_cache
        self.last_update = -1
        self.screen = screen
        self.empty = None
        self.buffer = screen.copy()
        self.tile_size = conf.tile_size
        self.start_time = time.time()

    def update(self, sim: Simulator, dt: float, board: Board) -> None:
        if board.has_effects or board.last_update > self.last_update:
            self.last_update = board.last_update
            if not self.empty:
                self.empty = self.screen.copy()
                draw_empty(board, self.empty, self.conf, self.tile_set, self.start_time)
            self.buffer.blit(self.empty, (0, 0))
            draw_tiles(board, self.buffer, self.conf, self.tile_set, self.start_time)

        # display game
        self.screen.blit(self.buffer, (0, 0))

        if self.conf.DEBUG_MODE:
            for x in range(board.width):
                for y in range(board.height):
                    cell = board.by_grid(Vector.create(x, y))
                    for p in cell.get(Player):
                        sprite: Sprite = p.get(Sprite)
                        self.screen.blit(self.graphics_cache.get_sprite(sprite)[0],
                                         _pos(self.conf, x, y, False, self.start_time))


def draw_empty(board: Board, empty: Surface, conf: GameConfig, tile_set: TileSet, start_time: float):
    for x in range(board.width):
        for y in range(board.height):
            empty.blit(conf.graphics_cache.get_image(tile_set.images[Tiles.EMPTY]), _pos(conf, x, y, False, start_time))


def draw_tiles(board: Board, buffer: Surface, conf: GameConfig, tile_set: TileSet, start_time: float):
    for x in range(board.width):
        for y in range(board.height):
            cell = board.by_grid(Vector.create(x, y))
            image = tile_set.images[cell.tile]
            buffer.blit(conf.graphics_cache.get_image(image),
                        _pos(conf, x, y, cell.effect == TileEffect.SHAKING, start_time))


def _pos(conf: GameConfig, x: int, y: int, shaking: bool, start_time: float):
    offset_x = 0
    offset_y = 0
    if shaking:
        animation_time = (time.time() - start_time) % TILE_SHAKE_DURATION
        if TILE_SHAKE_DURATION / 8 < animation_time < TILE_SHAKE_DURATION / 8 * 2:
            offset_x = TILE_SHAKE_SIZE
        elif TILE_SHAKE_DURATION / 8 * 3 < animation_time < TILE_SHAKE_DURATION / 8 * 4:
            offset_y = TILE_SHAKE_SIZE
        elif TILE_SHAKE_DURATION / 8 * 5 < animation_time < TILE_SHAKE_DURATION / 8 * 6:
            offset_x = -TILE_SHAKE_SIZE
        elif TILE_SHAKE_DURATION / 8 * 7 < animation_time:
            offset_y = -TILE_SHAKE_SIZE
    return x * conf.tile_size.x + conf.playground_offset.x + offset_x, \
           y * conf.tile_size.y + conf.playground_offset.y + offset_y
