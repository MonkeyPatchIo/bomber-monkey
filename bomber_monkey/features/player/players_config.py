from typing import List

import pygame

from bomber_monkey.features.ia.flo.ia_flo import FloIA
from bomber_monkey.features.ia.ia_descriptor import IADescriptor
from bomber_monkey.features.ia.ia_key_binding import IAKeyBinding
from bomber_monkey.features.ia.ia_nico import NicoIA
from bomber_monkey.features.player.joystick_mapping import JoystickMapping
from bomber_monkey.features.player.keyboard_mapping import KeyboardMapping
from bomber_monkey.features.player.player_action import PlayerAction
from bomber_monkey.features.player.player_controller_descriptor import PlayerControllerDescriptor
from bomber_monkey.features.player.player_slot import PlayerSlot
from bomber_monkey.game_inputs import get_game_inputs
from bomber_monkey.utils.vector import Vector

MAX_PLAYER_NUMBER = 4

COLORS = [
    (255, 0, 0),
    (0, 0, 255),
    (0, 255, 0),
    (255, 255, 0),
]
STARTING_POSITIONS = [
    (1, 1),
    (-1, -1),
    (1, -1),
    (-1, 1),
]


def keyboard_controllers():
    return [
        PlayerControllerDescriptor(
            name="Keyboard ZQSD/SPACE",
            input_mapping=KeyboardMapping(
                down_key=pygame.K_s,
                up_key=pygame.K_z,
                left_key=pygame.K_q,
                right_key=pygame.K_d,
                action_key=pygame.K_SPACE,
                cancel_key=pygame.K_ESCAPE
            )),
        PlayerControllerDescriptor(
            name="Keyboard ARROWS/RETURN",
            input_mapping=KeyboardMapping(
                down_key=pygame.K_DOWN,
                up_key=pygame.K_UP,
                left_key=pygame.K_LEFT,
                right_key=pygame.K_RIGHT,
                action_key=pygame.K_RETURN,
                cancel_key=pygame.K_ESCAPE
            )
        )
    ]


def joystick_controllers():
    return [
        PlayerControllerDescriptor(
            name=joystick.get_name(),
            input_mapping=JoystickMapping(joystick.get_instance_id())
        )

        for joystick in map(
            pygame.joystick.Joystick,
            range(min(MAX_PLAYER_NUMBER,
                      pygame.joystick.get_count()))
        )
    ]


class PlayersConfig:
    def __init__(self):
        self.focused_controller = 0

        self.descriptors = [
            *keyboard_controllers(),
            *joystick_controllers()
        ]

        self.ia_descriptors: List[IADescriptor] = [
            IADescriptor("Nico", "N", pygame.K_n, lambda: NicoIA()),
            IADescriptor("Flo", "F", pygame.K_f, lambda: FloIA())
        ]

        self.ia_key_bindings = [
            IAKeyBinding("1", "2", pygame.K_1, pygame.K_2),
            IAKeyBinding("3", "4", pygame.K_3, pygame.K_4),
            IAKeyBinding("5", "6", pygame.K_5, pygame.K_6),
            IAKeyBinding("7", "8", pygame.K_7, pygame.K_8)
        ]

        self.slots = [
            PlayerSlot(
                player_id=0,
                start_pos=Vector.create(*starting_position),
                color=color
            )
            for (i, (starting_position, color)) in enumerate(zip(STARTING_POSITIONS, COLORS))
        ]

        # self.descriptors = [
        #     self.ia_descriptors[0],
        #     self.ia_descriptors[1]
        # ]

        self.active_descriptors = [
            # by default, the two keyboards
            self.descriptors[0],
            self.descriptors[1],
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
