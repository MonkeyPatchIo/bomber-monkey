import math

import pygame as pg
import pygameMenu

from bomber_monkey.features.board.board import Board
from bomber_monkey.game_config import GameConfig
from python_ecs.ecs import System, Simulator

TEXT_COLOR = (0, 176, 240)
FONT_SIZE = 150


class StartupCountDownDisplaySystem(System):
    def __init__(self, screen):
        super().__init__([Board])
        self.screen = screen

    def update(self, sim: Simulator, dt: float, board: Board) -> None:
        conf: GameConfig = sim.context.conf
        count_down = conf.game_startup_delay - int(sim.context.game_elapsed_time)
        if count_down >= 0:
            text = str(count_down) if count_down > 0 else "Go"

            ratio = sim.context.game_elapsed_time - int(sim.context.game_elapsed_time)
            ratio = min(ratio * 3, 1.0)
            font_size = int(FONT_SIZE * math.sin(ratio * math.pi / 2))

            font = pg.font.Font(pygameMenu.font.FONT_8BIT, font_size)
            text_x = conf.pixel_size.x / 2 - len(text) * font_size / 2
            text_y = conf.pixel_size.y / 2 - font_size / 2

            if count_down == 1:
                # special case for '1' since it is not centered in the font
                text_x += font_size / 4

            rendered_text = font.render(text, 1, TEXT_COLOR)
            self.screen.blit(rendered_text, (text_x, text_y))
