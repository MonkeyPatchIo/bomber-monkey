import pygame as pg
import pygameMenu

from bomber_monkey.features.player.player import Player
from bomber_monkey.game_config import GameConfig
from python_ecs.ecs import System


class TitleDisplaySystem(System):
    def __init__(self, conf: GameConfig, screen):
        super().__init__([Player])
        self.conf = conf
        self.screen = screen
        self.font_35 = pg.font.Font(pygameMenu.fonts.FONT_8BIT, 35)
        self.font_20 = pg.font.Font(pygameMenu.fonts.FONT_8BIT, 20)

    def update(self, dt: float, player: Player) -> None:
        self.screen.fill((0, 0, 0), pg.rect.Rect((0, 0), (self.conf.pixel_size.x, self.conf.playground_offset.y)))

        text = self.font_35.render('Bomber Monkey', 1, (0, 176, 240))
        self.screen.blit(text, (360, 3))

        text = self.font_20.render('by Monkey Patch', 1, (0, 176, 240))
        self.screen.blit(text, (400, 50))
