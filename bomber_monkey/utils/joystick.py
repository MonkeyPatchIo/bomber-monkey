import pygame as pg


def any_joystick_button(first_button=0, last_button=None) -> bool:
    for _ in range(pg.joystick.get_count()):
        joystick = pg.joystick.Joystick(_)
        if not last_button:
            for _ in range(first_button, joystick.get_numbuttons()):
                if joystick.get_button(_):
                    return True
        else:
            for _ in range(0, last_button):
                if joystick.get_button(_):
                    return True
    return False
