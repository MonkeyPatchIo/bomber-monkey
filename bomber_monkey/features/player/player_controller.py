from enum import IntEnum
from typing import Callable

import pygame

from python_ecs.ecs import Component


class PlayerAction(IntEnum):
    NONE = 0
    MOVE_LEFT = 1
    MOVE_RIGHT = 2
    MOVE_UP = 4
    MOVE_DOWN = 8
    SPECIAL_ACTION = 16


PlayerActioner = Callable[[], PlayerAction]


class PlayerController(Component):

    def __init__(self, impl: PlayerActioner):
        super().__init__()
        self.impl = impl

    def get_action(self) -> PlayerAction:
        return self.impl()


def keyboard_actioner(left_key, right_key, up_key, down_key, action_key) -> PlayerActioner:
    actions = {
        left_key: PlayerAction.MOVE_LEFT,
        right_key: PlayerAction.MOVE_RIGHT,
        up_key: PlayerAction.MOVE_UP,
        down_key: PlayerAction.MOVE_DOWN,
        action_key: PlayerAction.SPECIAL_ACTION,
    }

    def get_action() -> PlayerAction:
        keys = pygame.key.get_pressed()
        for k, action in actions.items():
            if k and keys[k]:
                return action
        return PlayerAction.NONE

    return get_action


JOYSTICK_THRESHOLD = .5


def joystick_actioner(joystick, axis_x, axis_y) -> PlayerActioner:

    def get_action() -> PlayerAction:
        action = PlayerAction.NONE

        if joystick.get_numaxes() >= 2:
            axis_0 = joystick.get_axis(0) * (-1 if axis_x else 1)
            axis_1 = joystick.get_axis(1) * (-1 if axis_y else 1)
            action |= handle_axis(axis_0, axis_1)

        if joystick.get_numhats() >= 1:
            axis_0, axis_1 = joystick.get_hat(0)
            axis_0 *= (-1 if axis_x else 1)
            axis_1 *= (-1 if axis_y else 1)
            action |= handle_axis(axis_0, -axis_1)

        for _ in range(0, joystick.get_numbuttons()):
            if joystick.get_button(_):
                action |= PlayerAction.SPECIAL_ACTION

        return action

    def handle_axis(axis_0, axis_1):
        action = PlayerAction.NONE
        if axis_0 < -JOYSTICK_THRESHOLD:
            action |= PlayerAction.MOVE_LEFT
        if axis_0 > JOYSTICK_THRESHOLD:
            action |= PlayerAction.MOVE_RIGHT
        if axis_1 < -JOYSTICK_THRESHOLD:
            action |= PlayerAction.MOVE_UP
        if axis_1 > JOYSTICK_THRESHOLD:
            action |= PlayerAction.MOVE_DOWN
        return action

    return get_action