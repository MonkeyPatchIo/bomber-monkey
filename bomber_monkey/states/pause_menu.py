import pygame as pg
import pygameMenu
from pygame.constants import QUIT
from pygameMenu.locals import PYGAME_MENU_EXIT

from bomber_monkey.entity_factory import GameFactory
from bomber_monkey.game_config import GameConfig
from bomber_monkey.states.app_state import AppState
from bomber_monkey.states.state import State
from bomber_monkey.states.state_manager import StateManager


class PauseMenuState(State):
    def __init__(self, state_manager: StateManager, conf: GameConfig, factory: GameFactory, screen):
        super().__init__()
        self.state_manager = state_manager
        self.conf = conf
        self.factory = factory
        self.screen = screen
        self.menu = None

    def init(self):
        self.menu = pygameMenu.Menu(
            self.screen,
            *self.conf.pixel_size.as_ints(),
            font=pygameMenu.fonts.FONT_8BIT,
            title='Pause',
            dopause=False
        )
        self.menu.add_option('Back to game', lambda: self.state_manager.change_state(AppState.IN_GAME))
        self.menu.add_option('Main menu', lambda: self.state_manager.change_state(AppState.MAIN_MENU))
        self.menu.add_option('Exit', PYGAME_MENU_EXIT)

    def _run(self):
        events = pg.event.get()
        for event in events:
            if event.type == QUIT:
                exit()
            if event.type == pg.KEYUP and event.key == pg.K_ESCAPE:
                self.state_manager.change_state(AppState.IN_GAME)
                break
        self.menu.mainloop(events)
        pg.display.flip()
