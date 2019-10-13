from typing import List

import pygame

from bomber_monkey.features.ia.ia import ia_actioner
from bomber_monkey.features.player.player_controller import joystick_actioner, PlayerActioner, keyboard_actioner, \
    PlayerAction
from bomber_monkey.features.player.player_slot import PlayerSlot
from bomber_monkey.utils.vector import Vector

MAX_PLAYER_NUMBER = 4
INVERT_X = [False, True, False]
INVERT_Y = [False, False, False]


class PlayerControllerDescriptor:
    def __init__(self, name: str, actioner: PlayerActioner):
        self.name = name
        self.actioner = actioner


class PlayersConfig:

    def __init__(self):
        self.descriptors: List[PlayerControllerDescriptor] = []
        self.descriptors.append(PlayerControllerDescriptor("Keyboard ZQSD/SPACE", keyboard_actioner(
            down_key=pygame.K_s,
            up_key=pygame.K_z,
            left_key=pygame.K_q,
            right_key=pygame.K_d,
            action_key=pygame.K_SPACE
        )))
        self.descriptors.append(PlayerControllerDescriptor("Keyboard ARROWS/RETURN", keyboard_actioner(
            down_key=pygame.K_DOWN,
            up_key=pygame.K_UP,
            left_key=pygame.K_LEFT,
            right_key=pygame.K_RIGHT,
            action_key=pygame.K_RETURN
        )))
        for i in range(min(4, pygame.joystick.get_count())):
            joystick = pygame.joystick.Joystick(i)
            if joystick:
                actioner = joystick_actioner(joystick, INVERT_X[i], INVERT_Y[i])
                self.descriptors.append(PlayerControllerDescriptor("Joystick " + str(i), actioner))

        self.descriptors.append(PlayerControllerDescriptor("IA 1", ia_actioner(down_key=pygame.K_s,
                                                                               up_key=pygame.K_z)))
        self.descriptors.append(PlayerControllerDescriptor("IA 2", ia_actioner(down_key=pygame.K_DOWN,
                                                                               up_key=pygame.K_UP)))

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
    def slot_and_actioners(self):
        for i in range(len(self.active_descriptors)):
            yield (self.slots[i], self.active_descriptors[i].actioner)


def menu_wait(players_config: PlayersConfig):
    nb_controllers = len(players_config.descriptors)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.JOYAXISMOTION or event.type == pygame.KEYUP or event.type == pygame.JOYBUTTONUP:
            key = event.key if event.type == pygame.KEYUP else None
            button = (event.joy, event.button) if event.type == pygame.JOYBUTTONUP else None
            for i in range(nb_controllers):
                descriptor = players_config.descriptors[i]
                action = descriptor.actioner(None, None, key, button)
                if action & PlayerAction.SPECIAL_ACTION:
                    yield i, PlayerAction.SPECIAL_ACTION
                if action & PlayerAction.MOVE_LEFT:
                    yield i, PlayerAction.MOVE_LEFT
                if action & PlayerAction.MOVE_RIGHT:
                    yield i, PlayerAction.MOVE_RIGHT
    return None
