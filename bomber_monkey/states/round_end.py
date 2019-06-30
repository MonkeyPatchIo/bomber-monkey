import pygame as pg
import pygameMenu

from bomber_monkey.features.player.player import Player
from bomber_monkey.states.app_state import AppState
from bomber_monkey.states.state import State


class RoundEndState(State):
    def __init__(self, app: 'App', winner: Player = None):
        super().__init__()
        self.app = app
        self.winner = winner
        self.menu = None

    def init(self):
        self.menu = pygameMenu.TextMenu(
            self.app.screen,
            *self.app.conf.pixel_size.as_ints(),
            font=pygameMenu.fonts.FONT_8BIT,
            title='Good Job',
            dopause=False
        )
        self.menu.add_line("Player {} scored".format(self.winner.player_id))

    def _run(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.KEYUP and (event.key == pg.K_ESCAPE or event.key == pg.K_RETURN):
                self.app.set_state(AppState.IN_GAME, self.app.states[AppState.IN_GAME])
        self.menu.mainloop(events)
        pg.display.flip()
