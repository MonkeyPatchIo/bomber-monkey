import pygame as pg
import pygameMenu

from bomber_monkey.features.board.board import Board
from bomber_monkey.features.display.image import Image
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.game_config import BLUE_MONKEY_COLOR, BLACK_COLOR, WHITE_COLOR, GameConfig
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import System, Simulator

TITLE_FONT_SIZE = 35
TITLE = "Bomber Monkey"
MARGIN = 3
SUBTITLE_FONT_SIZE = 20
SUBTITLE_PREFIX = "by "
SUBTITLE_PICTURE_SIZE = Vector.create(230, 46)
SUBTITLE_SIZE = Vector.create((len(SUBTITLE_PREFIX)) * SUBTITLE_FONT_SIZE, 0) + SUBTITLE_PICTURE_SIZE
SUBTITLE_TEXT_OFFSET = 5

class TitleBarDisplaySystem(System):
    def __init__(self, conf: GameConfig, screen):
        super().__init__([Board])
        self.conf = conf
        self.screen = screen
        font_title = pg.font.Font(pygameMenu.font.FONT_8BIT, TITLE_FONT_SIZE)
        self.font_subtitle = pg.font.Font(pygameMenu.font.FONT_8BIT, SUBTITLE_FONT_SIZE)
        self.rendered_title = font_title.render(TITLE, 1, BLUE_MONKEY_COLOR)
        self.title_pos = Vector.create(conf.pixel_size.x / 2 - (len(TITLE) * TITLE_FONT_SIZE) / 2, MARGIN)
        self.rendered_subtitle = self.font_subtitle.render(SUBTITLE_PREFIX, 1, BLUE_MONKEY_COLOR)
        self.monkeypatch = pg.transform.scale(
            conf.graphics_cache.get_image(Image(conf.media_path("monkeypatch.png"))),
            SUBTITLE_PICTURE_SIZE.as_ints())
        self.subtitle_pos = Vector.create(conf.pixel_size.x / 2 - SUBTITLE_SIZE.x / 2, MARGIN * 2 + TITLE_FONT_SIZE)
        self.subtitle_text_pos = self.subtitle_pos + Vector.create(0, SUBTITLE_PICTURE_SIZE.y - SUBTITLE_FONT_SIZE - SUBTITLE_TEXT_OFFSET)
        self.subtitle_pic_pos = self.subtitle_pos + Vector.create((len(SUBTITLE_PREFIX)) * SUBTITLE_FONT_SIZE, 0)

    def update(self, sim: Simulator, dt: float, board: Board) -> None:
        self.screen.fill(BLACK_COLOR,
                         pg.rect.Rect((0, 0), (sim.context.conf.pixel_size.x, sim.context.conf.playground_offset.y)))

        self.display_title()
        if sim.context.conf.DEBUG_MODE:
            self.display_fps(sim.context.clock, sim.context.board)

    def display_title(self):
        self.screen.blit(self.rendered_title, self.title_pos.as_ints())
        self.screen.blit(self.rendered_subtitle, self.subtitle_text_pos.as_ints())
        self.screen.blit(self.monkeypatch, self.subtitle_pic_pos.as_ints())

    def display_fps(self, clock, board: Board):
        fps = clock.get_fps()

        body1: RigidBody = board.players[0].get(RigidBody)
        body2: RigidBody = board.players[1].get(RigidBody)
        message = 'fps={:2.2f} P1\.speed=({:2.2f},{:2.2f}) P2\.speed=({:2.2f},{:2.2f})'.format(
            fps,
            body1.speed.x, body1.speed.y,
            body2.speed.x, body2.speed.y
        )
        text = self.font_subtitle.render(message, 1, WHITE_COLOR)

        self.screen.fill(BLACK_COLOR, pg.rect.Rect((0, TITLE_FONT_SIZE + 2 * MARGIN),
                                                   (self.conf.pixel_size.x, SUBTITLE_FONT_SIZE)))
        self.screen.blit(text, (0, TITLE_FONT_SIZE + 2 * MARGIN))
