import pygame

from bomber_monkey.features.controller.controller_descriptor import ControllerDescriptor
from bomber_monkey.features.controller.mappings.ia_mapping import IAMapping
from bomber_monkey.features.controller.mappings.joystick_mapping import JoystickMapping
from bomber_monkey.features.controller.mappings.keyboard_mapping import KeyboardMapping
from bomber_monkey.features.ia.flo.ia_flo import FloIA
from bomber_monkey.features.ia.nico.ia_nico import NicoIA
from bomber_monkey.features.player.player_action import PlayerAction
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
        ControllerDescriptor(
            name="Keyboard ZQSD/SPACE",
            factory=lambda: KeyboardMapping(
                down_key=pygame.K_s,
                up_key=pygame.K_z,
                left_key=pygame.K_q,
                right_key=pygame.K_d,
                action_key=pygame.K_SPACE,
                cancel_key=pygame.K_ESCAPE
            )),
        ControllerDescriptor(
            name="Keyboard ARROWS/RETURN",
            factory=lambda: KeyboardMapping(
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
    controllers = []
    for i in range(min(MAX_PLAYER_NUMBER, pygame.joystick.get_count())):
        joystick = pygame.joystick.Joystick(i)
        if joystick:
            controllers.append(ControllerDescriptor(
                name=joystick.get_name(),
                factory=lambda: JoystickMapping(
                    joystick.get_instance_id()
                )
            ))
    return controllers


class PlayersConfig:
    def __init__(self):
        self.focused_controller = 0

        self.descriptors = [
            *keyboard_controllers(),
            *joystick_controllers()
        ]
        self.ia_descriptors = []

        self.ia_templates = {
            pygame.K_n: ("Nico", lambda: IAMapping(NicoIA())),
            pygame.K_f: ("Flo", lambda: IAMapping(FloIA()))
        }

        self.slots = [
            PlayerSlot(
                player_id=0,
                start_pos=Vector.create(*starting_position),
                color=color
            )
            for (i, (starting_position, color)) in enumerate(zip(STARTING_POSITIONS, COLORS))
        ]

        self.active_controllers = [
            # by default, the two keyboards
            self.descriptors[0],
            self.descriptors[1],
        ]

    @property
    def nb_players(self):
        return len(self.active_controllers)

    @property
    def slot_and_input_mapping(self):
        for i in range(len(self.active_controllers)):
            yield self.slots[i], self.active_controllers[i].input_mapping


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
