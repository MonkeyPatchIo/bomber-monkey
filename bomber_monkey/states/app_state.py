from enum import IntEnum
from typing import Dict, Tuple, Any, Optional, Callable


class AppState:

    def run(self) -> Tuple[IntEnum, Any]:
        raise NotImplementedError()

    def stop(self):
        pass


AppTransition = Callable[[Any], AppState]


class AppStateManager:

    def __init__(self, initial_transition: IntEnum, transitions: Dict[IntEnum, AppTransition]):
        self.initial_transition = initial_transition
        self.transitions = transitions
        self.state: Optional[AppState] = None

    def run(self):
        self.state: AppState = self.transitions[self.initial_transition](None)
        while True:
            transition_request = self.state.run()
            if transition_request is not None:
                self.state.stop()
                self.state = self.transitions[transition_request[0]](transition_request[1])


class AppTransitions(IntEnum):
    MAIN_MENU = 1
    NEW_GAME = 2
    RESUME_GAME = 3
    PAUSE_MENU = 4
    ROUND_END = 5
    GAME_END = 6
