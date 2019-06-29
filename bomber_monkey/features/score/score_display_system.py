from pygame.rect import Rect

from bomber_monkey.features.score.scores import Scores
from bomber_monkey.game_config import GameConfig
from python_ecs.ecs import System
import pygame as pg
import pygameMenu


class ScoresDisplaySystem(System):
    def __init__(self, conf: GameConfig, screen):
        super().__init__([Scores])
        self.conf = conf
        self.screen = screen
        self.font = pg.font.Font(pygameMenu.fonts.FONT_8BIT, 35)
        self.font2 = pg.font.Font(pygameMenu.fonts.FONT_8BIT, 20)

    def update(self, scores: Scores) -> None:
        self.screen.fill((0, 0, 0), Rect((0, 0), (self.conf.pixel_size.x, self.conf.playground_offset.y)))
        text = self.font.render(str(scores.scores[0]), 1, (255, 255, 255))
        self.screen.blit(text, (5, 3))
        text = self.font.render(str(scores.scores[1]), 1, (255, 255, 255))
        self.screen.blit(text, (self.conf.pixel_size.x - 45, 3))

        text = self.font.render('Bomber Monkey', 1, (255, 255, 255))
        self.screen.blit(text, (360, 3))

        text = self.font2.render('by Monkey Patch', 1, (255, 255, 255))
        self.screen.blit(text, (400, 50))
