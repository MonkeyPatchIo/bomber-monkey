import pygame as pg
import pygameMenu
from pygame.constants import QUIT
from pygameMenu.locals import PYGAME_MENU_EXIT

from bomber_monkey.game_config import GameConfig
from bomber_monkey.states.app_state import AppState
from bomber_monkey.states.in_game import GameState
from bomber_monkey.states.state import State
from bomber_monkey.states.state_manager import StateManager
from bomber_monkey.game_systems import systems_provider


class MainMenuState(State):
    def __init__(self, state_manager: StateManager, conf: GameConfig, screen):
        super().__init__()
        self.state_manager = state_manager
        self.conf = conf
        self.screen = screen
        self.menu = None

    def init(self):
        self.menu = pygameMenu.Menu(
            self.screen,
            *self.conf.pixel_size.as_ints(),
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
        game_state = GameState(self.state_manager, self.conf, self.screen, systems_provider)
        self.state_manager.states[AppState.IN_GAME] = game_state
        self.state_manager.change_state(AppState.IN_GAME)
