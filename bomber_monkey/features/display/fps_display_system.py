import pygame as pg
import pygameMenu

from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.player.player import Player
from bomber_monkey.game_factory import GameFactory
from python_ecs.ecs import System


class FpsDisplaySystem(System):
    def __init__(self, factory: GameFactory, screen):
        super().__init__([Player])
        self.factory = factory
        self.conf = factory.conf
        self.screen = screen
        self.nb_frames = 0
        self.total_time = 0
        self.fps = 0

        self.font_35 = pg.font.Font(pygameMenu.fonts.FONT_8BIT, 35)
        self.font_20 = pg.font.Font(pygameMenu.fonts.FONT_8BIT, 20)

    def update(self, dt: float, player: Player) -> None:
        if not self.conf.debug_fps:
            return
        self.nb_frames += 1
        self.total_time += dt
        if self.total_time > 1:
            self.fps = self.nb_frames / self.total_time

        body1: RigidBody = self.factory.players[0].get(RigidBody)
        body2: RigidBody = self.factory.players[1].get(RigidBody)
        message = 'FPS: %.2f v1x=%.2f v1y=%.2f v2x=%.2f v2y=%.2f' % (
            self.fps, body1.speed.x, body1.speed.y, body2.speed.x, body2.speed.y)
        text = self.font_20.render(message, 1, (255, 255, 255))

        self.screen.fill((0, 0, 0), pg.rect.Rect((5, 50), (self.conf.pixel_size.x, 20)))
        self.screen.blit(text, (5, 50))
