from bomber_monkey.features.player.player import Player
from bomber_monkey.game_config import GameConfig
from python_ecs.ecs import System
import pygame as pg
import pygameMenu


class PlayerScoreDisplaySystem(System):
    def __init__(self, conf: GameConfig, screen):
        super().__init__([Player])
        self.conf = conf
        self.screen = screen
        self.font_35 = pg.font.Font(pygameMenu.fonts.FONT_8BIT, 35)

    def update(self, player: Player) -> None:
        text = self.font_35.render(str(player.score), 1, (255, 255, 255))

        pos = (5, 3) if player.player_id == 0 else (self.conf.pixel_size.x - 45, 3)
        self.screen.blit(text, pos)
