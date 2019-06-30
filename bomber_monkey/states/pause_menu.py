import pygame as pg
import pygameMenu
from pygame.constants import QUIT
from pygameMenu.locals import PYGAME_MENU_EXIT

from bomber_monkey.states.app_state import AppState
from bomber_monkey.states.state import State


class PauseMenuState(State):
    def __init__(self, app: 'App'):
        super().__init__()
        self.app = app
        self.menu = None

    def init(self):
        self.menu = pygameMenu.Menu(
            self.app.screen,
            *self.app.conf.pixel_size.as_ints(),
            font=pygameMenu.fonts.FONT_8BIT,
            title='Pause',
            dopause=False
        )
        self.menu.add_option('Back to game', lambda: self.app.set_state(AppState.IN_GAME))
        self.menu.add_option('Main menu', lambda: self.app.set_state(AppState.MAIN_MENU))
        self.menu.add_option('Exit', PYGAME_MENU_EXIT)

    def _run(self):
        events = pg.event.get()
        for event in events:
            if event.type == QUIT:
                exit()
            if event.type == pg.KEYUP and event.key == pg.K_ESCAPE:
                self.app.set_state(AppState.IN_GAME)
                break
        self.menu.mainloop(events)
        pg.display.flip()
