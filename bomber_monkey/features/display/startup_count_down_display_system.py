import pygame as pg
import pygameMenu

from bomber_monkey.features.board.board import Board
from bomber_monkey.game_config import GameConfig
from python_ecs.ecs import System, Simulator

TEXT_COLOR = (0, 176, 240)
FONT_SIZE = 150


class StartupCountDownDisplaySystem(System):
    def __init__(self, conf: GameConfig, screen):
        super().__init__([Board])
        self.screen = screen
        self.font = pg.font.Font(pygameMenu.font.FONT_8BIT, FONT_SIZE)
        self.text_x = conf.pixel_size.x / 2
        self.text_y = conf.pixel_size.y / 2 - FONT_SIZE / 2

    def update(self, sim: Simulator, dt: float, board: Board) -> None:
        conf: GameConfig = sim.context.conf
        count_down = conf.game_startup_delay - int(sim.context.game_elasped_time)
        if count_down >= 0:
            text = str(count_down) if count_down > 0 else "Go"
            rendered_text = self.font.render(text, 1, TEXT_COLOR)
            self.screen.blit(rendered_text, (self.text_x - len(text) * FONT_SIZE / 2, self.text_y))
