from enum import Enum
from typing import Dict

from bomber_monkey.states.app_state import AppState
from bomber_monkey.states.state import State


class StateManager(object):
    def __init__(self, ):
        self.current_state = None
        self.states: Dict[Enum, State] = None

    def init(self, states: Dict[Enum, State]):
        self.states = states

    def change_state(self, state_type: AppState, state: State = None):
        if not state:
            state = self.states[state_type]

        if self.current_state:
            self.current_state.stop()
        state.init()
        self.current_state = state
