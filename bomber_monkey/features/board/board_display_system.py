import time

import pygameMenu
import pygame as pg

from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.game_config import GameConfig
from bomber_monkey.states.in_game import GameState
from bomber_monkey.utils.image_loader import ImageLoader
from bomber_monkey.features.board.board import Board, Tiles
from bomber_monkey.features.display.image import Image
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import System


class BoardDisplaySystem(System):
    def __init__(self, conf: GameConfig, state: GameState, image_loader: ImageLoader, screen, tile_size: Vector,
                 tile_set: str = 'jungle'):
        super().__init__([Board])
        self.conf = conf
        self.state = state
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
        self.font_35 = pg.font.Font(pygameMenu.fonts.FONT_8BIT, 35)
        self.font_20 = pg.font.Font(pygameMenu.fonts.FONT_8BIT, 20)
        self.nb_frames = 0
        self.start_time = time.time()

    def update(self, board: Board) -> None:
        if board.last_update > self.last_update:
            self.last_update = board.last_update
            if not self.empty:
                self.empty = self.screen.copy()
                for x in range(board.width):
                    for y in range(board.height):
                        self.empty.blit(self.image_loader[self.images[Tiles.EMPTY]], self._pos(x, y))
            self.buffer.blit(self.empty, (0, 0))
            for x in range(board.width):
                for y in range(board.height):
                    self.buffer.blit(self.image_loader[self._image(board, x, y)], self._pos(x, y))

        # display game
        self.screen.blit(self.buffer, (0, 0))

        # title bar
        self.screen.fill((0, 0, 0), pg.rect.Rect((0, 0), (self.conf.pixel_size.x, self.conf.playground_offset.y)))
        text = self.font_35.render('Bomber Monkey', 1, (0, 176, 240))
        self.screen.blit(text, (360, 3))
        if not self.conf.debug_fps:
            text = self.font_20.render('by Monkey Patch', 1, (0, 176, 240))
            self.screen.blit(text, (400, 50))
        else:
            self.nb_frames += 1
            fps = self.nb_frames / (time.time() - self.start_time)
            body1: RigidBody = self.state.players[0].get(RigidBody)
            body2: RigidBody = self.state.players[1].get(RigidBody)
            message = 'FPS: %.2f v1x=%.2f v1y=%.2f v2x=%.2f v2y=%.2f' % (fps, body1.speed.x, body1.speed.y, body2.speed.x, body2.speed.y)
            text = self.font_20.render(message, 1, (255, 255, 255))
            self.screen.blit(text, (5, 50))


    def _pos(self, x, y):
        return x * self.tile_size.x + self.conf.playground_offset.x, y * self.tile_size.y + self.conf.playground_offset.y

    def _image(self, board: Board, x: int, y: int) -> Image:
        cell = board.by_grid(Vector.create(x, y))
        tile = cell.tile
        return self.images[tile]
