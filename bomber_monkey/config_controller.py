import pygame as pg

from bomber_monkey.features.player.player_controller import PlayerController
from bomber_monkey.game_config import GameConfig


def controller_provider(conf: GameConfig):
    controllers = [
        PlayerController.from_keyboard(
            conf.player_speed,
            down_key=pg.K_s,
            up_key=pg.K_z,
            left_key=pg.K_q,
            right_key=pg.K_d,
            action_key=pg.K_SPACE
        ),
        PlayerController.from_keyboard(
            conf.player_speed,
            down_key=pg.K_DOWN,
            up_key=pg.K_UP,
            left_key=pg.K_LEFT,
            right_key=pg.K_RIGHT,
            action_key=pg.K_KP0
        ),

        PlayerController.from_keyboard(
            conf.player_speed,
            down_key=pg.K_DOWN,
            up_key=pg.K_UP,
            left_key=pg.K_LEFT,
            right_key=pg.K_RIGHT,
            action_key=pg.K_KP0
        ),

        PlayerController.from_keyboard(
            conf.player_speed,
            down_key=pg.K_DOWN,
            up_key=pg.K_UP,
            left_key=pg.K_LEFT,
            right_key=pg.K_RIGHT,
            action_key=pg.K_KP0
        )
    ]
    pg.joystick.init()
    for i in range(min(4, pg.joystick.get_count())):
        controllers[i] = PlayerController.from_joystick(
            conf.player_speed,
            pg.joystick.Joystick(i),
            conf.INVERT_X[i],
            conf.INVERT_Y[i])

    return controllers
