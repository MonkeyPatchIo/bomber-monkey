from typing import List

import pygame

from bomber_monkey.features.player.ia_controller_system import IAMapping
from bomber_monkey.features.player.player_action import InputMapping, PlayerAction
from bomber_monkey.features.player.player_slot import PlayerSlot
from bomber_monkey.features.player.user_input_mapping import KeyboardMapping, JoystickMapping
from bomber_monkey.game_inputs import get_game_inputs
from bomber_monkey.utils.vector import Vector

MAX_PLAYER_NUMBER = 4


class PlayerControllerDescriptor:
    def __init__(self, name: str, input_mapping: InputMapping):
        self.name = name
        self.input_mapping = input_mapping


class PlayersConfig:

    def __init__(self):
        self.descriptors: List[PlayerControllerDescriptor] = []
        self.descriptors.append(PlayerControllerDescriptor("Keyboard ZQSD/SPACE", KeyboardMapping(
            down_key=pygame.K_s,
            up_key=pygame.K_z,
            left_key=pygame.K_q,
            right_key=pygame.K_d,
            action_key=pygame.K_SPACE,
            cancel_key=pygame.K_ESCAPE
        )))
        self.descriptors.append(PlayerControllerDescriptor("Keyboard ARROWS/RETURN", KeyboardMapping(
            down_key=pygame.K_DOWN,
            up_key=pygame.K_UP,
            left_key=pygame.K_LEFT,
            right_key=pygame.K_RIGHT,
            action_key=pygame.K_RETURN,
            cancel_key=pygame.K_ESCAPE
        )))
        for i in range(min(MAX_PLAYER_NUMBER, pygame.joystick.get_count())):
            joystick = pygame.joystick.Joystick(i)
            if joystick:
                actioner = JoystickMapping(joystick.get_instance_id())
                self.descriptors.append(PlayerControllerDescriptor(joystick.get_name(), actioner))

        self.descriptors.append(PlayerControllerDescriptor("IA 1", IAMapping(left_key=pygame.K_s,
                                                                             right_key=pygame.K_z)))
        self.descriptors.append(PlayerControllerDescriptor("IA 2", IAMapping(left_key=pygame.K_DOWN,
                                                                             right_key=pygame.K_UP)))

        self.slots = [
            PlayerSlot(
                player_id=0,
                start_pos=Vector.create(1, 1),
                color=(255, 0, 0)
            ),
            PlayerSlot(
                player_id=1,
                start_pos=Vector.create(-1, -1),
                color=(0, 0, 255)
            ),
            PlayerSlot(
                player_id=2,
                start_pos=Vector.create(1, -1),
                color=(0, 255, 0)
            ),
            PlayerSlot(
                player_id=3,
                start_pos=Vector.create(-1, 1),
                color=(255, 255, 0)
            )
        ]

        self.active_descriptors = [
            # by default, the two keyboards
            self.descriptors[0],
            self.descriptors[1]
        ]

    @property
    def nb_players(self):
        return len(self.active_descriptors)

    @property
    def slot_and_input_mapping(self):
        for i in range(len(self.active_descriptors)):
            yield self.slots[i], self.active_descriptors[i].input_mapping


def menu_wait(players_config: PlayersConfig):
    nb_controllers = len(players_config.descriptors)
    for i in range(nb_controllers):
        descriptor = players_config.descriptors[i]
        action = descriptor.input_mapping.get_action(get_game_inputs(), menu=True)
        if action & PlayerAction.MAIN_ACTION:
            yield i, PlayerAction.MAIN_ACTION
        if action & PlayerAction.MOVE_LEFT:
            yield i, PlayerAction.MOVE_LEFT
        if action & PlayerAction.MOVE_RIGHT:
            yield i, PlayerAction.MOVE_RIGHT
    return None
