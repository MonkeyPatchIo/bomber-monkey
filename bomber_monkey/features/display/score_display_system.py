import pygame as pg
import pygameMenu

from bomber_monkey.features.player.player import Player
from bomber_monkey.game_config import GameConfig
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import System, Simulator

FONT_SIZE = 35
MARGIN = 5


class PlayerScoreDisplaySystem(System):
    def __init__(self, screen):
        super().__init__([Player])
        self.screen = screen
        self.font = pg.font.Font(pygameMenu.font.FONT_8BIT, FONT_SIZE)

    def update(self, sim: Simulator, dt: float, player: Player) -> None:
        conf: GameConfig = sim.context.conf
        text = self.font.render(str(sim.context.scores.scores[player.player_id]), 1, player.color)
        board_pos = player.slot.start_pos
        pos_x = Vector.create(0, 0)
        if board_pos.x < 0:
            pos_x = conf.pixel_size.x - FONT_SIZE - MARGIN
        else:
            pos_x = MARGIN
        if board_pos.y < 0:
            pos_y = conf.playground_offset.y - FONT_SIZE - MARGIN
        else:
            pos_y = MARGIN

        self.screen.blit(text, (pos_x, pos_y))
