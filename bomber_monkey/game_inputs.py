from typing import Dict, List

import pygame
from pygame.joystick import Joystick

from bomber_monkey.utils.joystick import get_joystick_mapping, get_joysticks, JoystickMapping


class ControllerInputs:
    def __init__(self):
        self.down = []
        self.up = []
        self.pressed = []


class GameInputs:
    def __init__(self) -> None:
        super().__init__()
        self.events = []
        self.keyboard = ControllerInputs()
        self.joysticks: Dict[int, ControllerInputs] = {}
        self.quit = False

    def is_up(self, key: int):
        if key in self.keyboard.up:
            return True
        for controller in self.joysticks.values():
            if key in controller.up:
                return True
        return False

    def is_down(self, key: int):
        if key in self.keyboard.down:
            return True
        for controller in self.joysticks.values():
            if key in controller.down:
                return True
        return False

    def is_pressed(self, key: int):
        if key in self.keyboard.pressed:
            return True
        for controller in self.joysticks.values():
            if key in controller.pressed:
                return True
        return False


previous_game_inputs = GameInputs()
game_inputs = GameInputs()


def get_game_inputs() -> GameInputs:
    return game_inputs


def refresh_game_inputs() -> GameInputs:
    global previous_game_inputs, game_inputs
    previous_game_inputs = game_inputs
    game_inputs = GameInputs()
    handle_events(game_inputs)
    handle_joysticks(game_inputs)
    compute_pressed_inputs(previous_game_inputs.keyboard, game_inputs.keyboard)
    fill_joysticks(previous_game_inputs.joysticks.keys(), game_inputs.joysticks)
    fill_joysticks(game_inputs.joysticks.keys(), previous_game_inputs.joysticks)
    for joystick_id, joystick in game_inputs.joysticks.items():
        previous_joystick = previous_game_inputs.joysticks[joystick_id]
        compute_up_down_inputs(previous_joystick, joystick)
    return game_inputs


def reset_game_inputs():
    global previous_game_inputs, game_inputs
    previous_game_inputs = GameInputs()
    game_inputs = GameInputs()


def handle_events(inputs: GameInputs) -> None:
    inputs.events = pygame.event.get()
    for event in inputs.events:
        if event.type == pygame.KEYDOWN:
            inputs.keyboard.down.append(event.key)
        if event.type == pygame.KEYUP:
            inputs.keyboard.up.append(event.key)
        if event.type == pygame.QUIT:
            inputs.quit = True


JOYSTICK_THRESHOLD = .5


def handle_joysticks(inputs: GameInputs):
    for joystick in get_joysticks():
        handle_joystick(inputs, joystick)


def handle_joystick(inputs: GameInputs, joystick: Joystick):
    joystick_mapping = get_joystick_mapping(joystick)
    joystick_inputs = ControllerInputs()

    check_joystick_buttons(joystick_inputs, joystick, joystick_mapping.ok_buttons, pygame.K_RETURN)
    check_joystick_buttons(joystick_inputs, joystick, joystick_mapping.cancel_buttons, pygame.K_ESCAPE)
    check_joystick_buttons(joystick_inputs, joystick, joystick_mapping.up_buttons, pygame.K_UP)
    check_joystick_buttons(joystick_inputs, joystick, joystick_mapping.down_buttons, pygame.K_DOWN)
    check_joystick_buttons(joystick_inputs, joystick, joystick_mapping.left_buttons, pygame.K_LEFT)
    check_joystick_buttons(joystick_inputs, joystick, joystick_mapping.right_buttons, pygame.K_RIGHT)

    for axe in joystick_mapping.axes:
        axis_0 = joystick.get_axis(axe[0]) * (-1 if axe[2] else 1)
        axis_1 = joystick.get_axis(axe[1]) * (-1 if axe[3] else 1)
        handle_joystick_axis(joystick_inputs, axis_0, axis_1)

    for hat in joystick_mapping.hats:
        axis_0, axis_1 = joystick.get_hat(hat[0])
        axis_0 *= (-1 if hat[1] else 1)
        axis_1 *= (-1 if hat[2] else 1)
        handle_joystick_axis(joystick_inputs, axis_0, -axis_1)

    inputs.joysticks[joystick.get_instance_id()] = joystick_inputs


def check_joystick_buttons(joystick_inputs: ControllerInputs, joystick: Joystick, buttons: List[int], key: int):
    for cancel_buttons in buttons:
        if joystick.get_button(cancel_buttons):
            joystick_inputs.pressed.append(key)


def handle_joystick_axis(joystick_input: ControllerInputs, axis_0: float, axis_1: float):
    if axis_0 < -JOYSTICK_THRESHOLD:
        joystick_input.pressed.append(pygame.K_LEFT)
    if axis_0 > JOYSTICK_THRESHOLD:
        joystick_input.pressed.append(pygame.K_RIGHT)
    if axis_1 < -JOYSTICK_THRESHOLD:
        joystick_input.pressed.append(pygame.K_UP)
    if axis_1 > JOYSTICK_THRESHOLD:
        joystick_input.pressed.append(pygame.K_DOWN)


def fill_joysticks(joysticks_ids, joysticks):
    for joystick_id in joysticks_ids:
        if joystick_id not in joysticks:
            joystick = ControllerInputs()
            joysticks[joystick_id] = joystick


def compute_pressed_inputs(previous_inputs: ControllerInputs, inputs: ControllerInputs):
    inputs.pressed = [key for key in previous_inputs.pressed if key not in inputs.up]
    for key in inputs.down:
        inputs.pressed.append(key)


def compute_up_down_inputs(previous_inputs: ControllerInputs, inputs: ControllerInputs):
    inputs.down = [key for key in inputs.pressed if key not in previous_inputs.pressed]
    inputs.up = [key for key in previous_inputs.pressed if key not in inputs.pressed]
