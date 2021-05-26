import functools
from typing import Dict

import pygame

from bomber_monkey.features.player.player_action import PlayerAction, InputMapping
from bomber_monkey.game_inputs import GameInputs, ControllerInputs
from python_ecs.ecs import Component


class UserInputMapping(InputMapping):
    def get_action(self, inputs: GameInputs, menu: bool) -> PlayerAction:
        pass

    @property
    def type_id(self) -> 'Component.Type':
        return UserInputMapping


def compute_action(move_actions: Dict[int, PlayerAction], tool_actions: Dict[int, PlayerAction], inputs: ControllerInputs, menu: bool):
    active_move_actions = [action for key, action in move_actions.items() if key in (inputs.up if menu else inputs.pressed)]
    active_tool_actions = [action for key, action in tool_actions.items() if key in inputs.up]
    result_action = functools.reduce(lambda a1, a2: a1 | a2, active_move_actions, PlayerAction.NONE)
    res = functools.reduce(lambda a1, a2: a1 | a2, active_tool_actions, result_action)
    return res


class KeyboardMapping(UserInputMapping):
    def __init__(self, left_key, right_key, up_key, down_key, action_key, cancel_key):
        super().__init__()
        self.move_actions = {
            left_key: PlayerAction.MOVE_LEFT,
            right_key: PlayerAction.MOVE_RIGHT,
            up_key: PlayerAction.MOVE_UP,
            down_key: PlayerAction.MOVE_DOWN
        }
        self.tool_actions = {
           action_key: PlayerAction.MAIN_ACTION,
           cancel_key: PlayerAction.CANCEL,
        }

    def get_action(self, inputs: GameInputs, menu: bool) -> PlayerAction:
        return compute_action(self.move_actions, self.tool_actions, inputs.keyboard, menu)


class JoystickMapping(UserInputMapping):
    def __init__(self, joystick_id: int):
        super().__init__()
        self.joystick_id = joystick_id
        self.move_actions = {
            pygame.K_LEFT: PlayerAction.MOVE_LEFT,
            pygame.K_RIGHT: PlayerAction.MOVE_RIGHT,
            pygame.K_UP: PlayerAction.MOVE_UP,
            pygame.K_DOWN: PlayerAction.MOVE_DOWN
        }
        self.tool_actions = {
            pygame.K_RETURN: PlayerAction.MAIN_ACTION,
            pygame.K_ESCAPE: PlayerAction.CANCEL,
        }

    def get_action(self, inputs: GameInputs, menu: bool) -> PlayerAction:
        if self.joystick_id not in inputs.joysticks:
            return PlayerAction.NONE
        joystick_input = inputs.joysticks[self.joystick_id]
        return compute_action(self.move_actions, self.tool_actions, joystick_input, menu)
