import pygame as pg
import pygameMenu

from bomber_monkey.features.player.player import Player
from python_ecs.ecs import System, Simulator


class PlayerScoreDisplaySystem(System):
    def __init__(self, screen):
        super().__init__([Player])
        self.screen = screen
        self.font_35 = pg.font.Font(pygameMenu.font.FONT_8BIT, 35)

    def update(self, sim: Simulator, dt: float, player: Player) -> None:
        text = self.font_35.render(str(sim.context.scores[player.player_id]), 1, player.color)
        pos = player.slot.score_pos
        self.screen.blit(text, pos)
