import time
from enum import Enum
from typing import Dict

import pygame as pg

from bomber_monkey.states.app_state import AppState
from bomber_monkey.states.state import State


class StateManager(object):
    def __init__(self):
        self.current_state = None
        self.states: Dict[Enum, State] = None

    def init(self, states: Dict[Enum, State]):
        self.states = states

    def change_state(self, state_type: AppState, state: State = None, init: bool = True, sleep: float = 0):

        if sleep > 0:
            time.sleep(sleep)

        if not state:
            state = self.states[state_type]

        if self.current_state:
            self.current_state.stop()

        if init:
            state.init()
        self.current_state = state
