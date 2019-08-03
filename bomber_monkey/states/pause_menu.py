import pygame as pg
import pygameMenu

from bomber_monkey.game_config import GameConfig
from bomber_monkey.states.app_state import AppState
from bomber_monkey.states.state import State
from bomber_monkey.states.state_manager import StateManager


class PauseMenuState(State):
    def __init__(self, state_manager: StateManager, conf: GameConfig, screen):
        super().__init__()
        self.state_manager = state_manager
        self.conf = conf
        self.screen = screen
        self.menu = pygameMenu.Menu(
            self.screen,
            *self.conf.pixel_size.as_ints(),
            font=pygameMenu.font.FONT_8BIT,
            title='Pause',
            dopause=False
        )
        self.menu.add_option('Back to game',
                             lambda: self.state_manager.change_state(AppState.IN_GAME, init=False, sleep=.5))
        self.menu.add_option('Main menu', lambda: self.state_manager.change_state(AppState.MAIN_MENU, init=False))
        self.menu.add_option('Exit', pygameMenu.events.EXIT)

    def init(self):
        pass

    def _run(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.KEYUP and event.key not in [pg.K_UP, pg.K_DOWN]:
                self.state_manager.change_state(AppState.IN_GAME, self.state_manager.states[AppState.IN_GAME],
                                                init=False, sleep=.5)
        self.menu.mainloop(events)
        pg.display.flip()
