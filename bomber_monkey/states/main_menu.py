import pygame as pg
import pygameMenu
from pygame.constants import QUIT
from pygameMenu.locals import PYGAME_MENU_EXIT

from bomber_monkey.game_config import GameConfig
from bomber_monkey.states.app_state import AppState
from bomber_monkey.states.game_state import GameState
from bomber_monkey.states.state import State
from bomber_monkey.states.state_manager import StateManager


class MainMenuState(State):
    def __init__(self, state_manager: StateManager, conf: GameConfig, screen):
        super().__init__()
        self.state_manager = state_manager
        self.conf = conf
        self.screen = screen
        self.menu = pygameMenu.Menu(
            self.screen,
            *self.conf.pixel_size.as_ints(),
            font=pygameMenu.fonts.FONT_8BIT,
            title='Bomber Monkey',
            dopause=False
        )
        self.menu.add_option('New game', self.new_game)
        self.menu.add_option('Exit', PYGAME_MENU_EXIT)

    def init(self):
        pass

    def _run(self):
        events = pg.event.get()
        self.menu.mainloop(events)
        pg.display.flip()

    def new_game(self):
        game_state = GameState(self.state_manager, self.conf, self.screen)
        self.state_manager.states[AppState.IN_GAME] = game_state
        self.state_manager.change_state(AppState.IN_GAME, sleep=.5)
