import pygame as pg
import pygameMenu

from bomber_monkey.features.board.board import Board
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.game_config import BLUE_MONKEY_COLOR, BLACK_COLOR, WHITE_COLOR, GameConfig
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import System, Simulator

TITLE_FONT_SIZE = 35
SUBTITLE_FONT_SIZE = 20
TITLE = "Bomber Monkey"
SUBTITLE = "by Monkey Patch"
MARGIN = 3


class TitleBarDisplaySystem(System):
    def __init__(self, conf: GameConfig, screen):
        super().__init__([Board])
        self.conf = conf
        self.screen = screen
        font_title = pg.font.Font(pygameMenu.font.FONT_8BIT, TITLE_FONT_SIZE)
        self.font_subtitle = pg.font.Font(pygameMenu.font.FONT_8BIT, SUBTITLE_FONT_SIZE)
        self.rendered_title = font_title.render(TITLE, 1, BLUE_MONKEY_COLOR)
        self.rendered_subtitle = self.font_subtitle.render(SUBTITLE, 1, BLUE_MONKEY_COLOR)
        self.title_pos = Vector.create(conf.pixel_size.x / 2 - (len(TITLE) * TITLE_FONT_SIZE) / 2, MARGIN)
        self.subtitle_pos = Vector.create(conf.pixel_size.x / 2 - (len(SUBTITLE) * SUBTITLE_FONT_SIZE) / 2, MARGIN * 2
                                          + TITLE_FONT_SIZE)

    def update(self, sim: Simulator, dt: float, board: Board) -> None:
        self.screen.fill(BLACK_COLOR,
                         pg.rect.Rect((0, 0), (sim.context.conf.pixel_size.x, sim.context.conf.playground_offset.y)))

        self.display_title()
        if sim.context.conf.DEBUG_MODE:
            self.display_fps(sim.context.clock, sim.context.board)

    def display_title(self):
        self.screen.blit(self.rendered_title, self.title_pos.as_ints())
        self.screen.blit(self.rendered_subtitle, self.subtitle_pos.as_ints())

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
