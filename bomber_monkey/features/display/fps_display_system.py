import time

import pygame as pg
import pygameMenu

from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.player.player import Player
from bomber_monkey.states.in_game import GameState
from python_ecs.ecs import System


class FpsDisplaySystem(System):
    def __init__(self, state: GameState, screen):
        super().__init__([Player])
        self.state = state
        self.conf = state.conf
        self.screen = screen
        self.nb_frames = 0
        self.start_time = time.time()

        self.font_35 = pg.font.Font(pygameMenu.fonts.FONT_8BIT, 35)
        self.font_20 = pg.font.Font(pygameMenu.fonts.FONT_8BIT, 20)

    def update(self, player: Player) -> None:
        if not self.conf.debug_fps:
            return
        self.nb_frames += 1
        fps = self.nb_frames / (time.time() - self.start_time)
        body1: RigidBody = self.state.players[0].get(RigidBody)
        body2: RigidBody = self.state.players[1].get(RigidBody)
        message = 'FPS: %.2f v1x=%.2f v1y=%.2f v2x=%.2f v2y=%.2f' % (
            fps, body1.speed.x, body1.speed.y, body2.speed.x, body2.speed.y)
        text = self.font_20.render(message, 1, (255, 255, 255))
        self.screen.blit(text, (5, 50))
