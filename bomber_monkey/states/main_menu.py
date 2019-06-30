import pygame as pg
import pygameMenu
from pygame.constants import QUIT
from pygameMenu.locals import PYGAME_MENU_EXIT

from bomber_monkey.states.app_state import AppState
from bomber_monkey.states.in_game import GameState
from bomber_monkey.states.state import State


class MainMenuState(State):
    def __init__(self, app: 'App'):
        super().__init__()
        self.app = app
        self.menu = None

    def init(self):
        self.menu = pygameMenu.Menu(
            self.app.screen,
            *self.app.conf.pixel_size.as_ints(),
            font=pygameMenu.fonts.FONT_8BIT,
            title='Bomber Monkey',
            dopause=False
        )
        self.menu.add_option('New game', self.new_game)
        self.menu.add_option('Exit', PYGAME_MENU_EXIT)

    def _run(self):
        events = pg.event.get()
        for event in events:
            if event.type == QUIT:
                exit()
        self.menu.mainloop(events)
        pg.display.flip()

    def new_game(self):
        game_state = GameState(self.app)
        self.app.states[AppState.IN_GAME] = game_state
        self.app.set_state(AppState.IN_GAME)
