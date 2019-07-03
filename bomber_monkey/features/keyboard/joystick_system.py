from bomber_monkey.features.keyboard.keymap import Keymap
from bomber_monkey.game_factory import GameFactory
from bomber_monkey.states.app_state import AppState
from bomber_monkey.utils.joystick import any_joystick_button
from python_ecs.ecs import System


class JoystickSystem(System):
    def __init__(self, factory: GameFactory):
        super().__init__([Keymap])
        self.factory = factory

    def update(self, dt: float, keymap: Keymap) -> None:
        if any_joystick_button(first_button=self.factory.conf.JOYSTICK_ESCAPE_BUTTON):
            self.factory.state_manager.change_state(AppState.PAUSE_MENU)
