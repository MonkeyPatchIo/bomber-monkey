import pygame as pg
import pygameMenu

from bomber_monkey.features.player.player import Player
from bomber_monkey.game_factory import GameFactory
from python_ecs.ecs import System, Simulator


class PlayerScoreDisplaySystem(System):
    def __init__(self, factory: GameFactory, screen):
        super().__init__([Player])
        self.factory = factory
        self.screen = screen
        self.font_35 = pg.font.Font(pygameMenu.fonts.FONT_8BIT, 35)

    @property
    def conf(self):
        return self.factory.conf

    def update(self, sim: Simulator, dt: float, player: Player) -> None:
        text = self.font_35.render(str(self.factory.game_state.scores[player.player_id]), 1, player.color)
        pos = player.slot.score_pos
        self.screen.blit(text, pos)
