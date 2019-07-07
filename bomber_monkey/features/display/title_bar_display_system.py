import pygame as pg
import pygameMenu

from bomber_monkey.features.board.board import Board
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.game_config import GameConfig
from python_ecs.ecs import System, Simulator

TEXT_COLOR = (0, 176, 240)


class TitleBarDisplaySystem(System):
    def __init__(self, conf: GameConfig, screen):
        super().__init__([Board])
        self.conf = conf
        self.screen = screen
        self.font_20 = pg.font.Font(pygameMenu.fonts.FONT_8BIT, 20)
        self.font_35 = pg.font.Font(pygameMenu.fonts.FONT_8BIT, 35)

    def update(self, sim: Simulator, dt: float, board: Board) -> None:
        self.screen.fill((0, 0, 0), pg.rect.Rect((0, 0), (self.conf.pixel_size.x, self.conf.playground_offset.y)))

        self.display_title()
        self.display_fps(sim.context.clock, sim.context.board)

    def display_title(self):
        text = self.font_35.render('Bomber Monkey', 1, TEXT_COLOR)
        self.screen.blit(text, (360, 3))
        text = self.font_20.render('by Monkey Patch', 1, TEXT_COLOR)
        self.screen.blit(text, (400, 50))

    def display_fps(self, clock, board: Board):
        if not self.conf.DEBUG_MODE:
            return

        fps = clock.get_fps()

        body1: RigidBody = board.players[0].get(RigidBody)
        body2: RigidBody = board.players[1].get(RigidBody)
        message = 'fps={:2.2f} P1\.speed=({:2.2f},{:2.2f}) P2\.speed=({:2.2f},{:2.2f})'.format(
            fps,
            body1.speed.x, body1.speed.y,
            body2.speed.x, body2.speed.y
        )
        text = self.font_20.render(message, 1, (255, 255, 255))

        self.screen.fill((0, 0, 0), pg.rect.Rect((50, 50), (self.conf.pixel_size.x - 100, 20)))
        self.screen.blit(text, (50, 50))
