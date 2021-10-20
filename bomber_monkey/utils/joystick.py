import math
from typing import List, Tuple

import pygame
from pygame.joystick import Joystick


joysticks = []


def init_joysticks():
    for _ in range(pygame.joystick.get_count()):
        joystick = pygame.joystick.Joystick(_)
        joystick.init()
        joysticks.append(joystick)


def get_joysticks():
    global joysticks
    return joysticks


class JoystickMapping:
    def __init__(self,
                 ok_buttons: List[int],
                 cancel_buttons: List[int],
                 up_buttons: List[int],
                 down_buttons: List[int],
                 left_buttons: List[int],
                 right_buttons: List[int],
                 axes: List[Tuple[int, int, bool, bool]],
                 hats: List[Tuple[int, bool, bool]]):
        self.ok_buttons = ok_buttons
        self.cancel_buttons = cancel_buttons
        self.up_buttons = up_buttons
        self.down_buttons = down_buttons
        self.left_buttons = left_buttons
        self.right_buttons = right_buttons
        self.axes = axes
        self.hats = hats


joystick_mappings = {
    # PS4 Controller
    # 0: X
    # 1: O
    # 2: []
    # 3: /\
    # 4: Share
    # 6: Options
    # 7: click pad left
    # 8: click pad right
    # 9: L1
    # 10: R1
    # 11: up
    # 12: down
    # 13: left
    # 14: right
    # 15: touch
    # Axe 0, 1: left pad x, y
    # Axe 2, 3: right pad x, y
    # Axe 4, 5: L2, R2
    "030000004c050000cc09000000016800": JoystickMapping(
        ok_buttons=[0, 1, 2, 3],
        cancel_buttons=[6, 15],
        up_buttons=[11],
        down_buttons=[12],
        left_buttons=[13],
        right_buttons=[14],
        axes=[(0, 1, False, False)],
        hats=[]
    ),

    # Logitech Dual Action
    # 0: X
    # 1: A
    # 2: B
    # 3: Y
    # 4: L1
    # 5: L2
    # 6: R1
    # 7: R2
    # 8: Back
    # 9: Start
    # 10: click left pad
    # 11: click left pad
    # Axe 0, 1: left pad x, y
    # Axe 2, 3: right pad x, y
    # Hat 1: arrows
    "030000006d04000016c2000000000000": JoystickMapping(
        ok_buttons=[0, 1, 2, 3],
        cancel_buttons=[8, 9],
        up_buttons=[],
        down_buttons=[],
        left_buttons=[],
        right_buttons=[],
        axes=[(0, 1, False, False)],
        hats=[(0, False, False)]
    )
}


default_joystick_mapping = JoystickMapping(
    ok_buttons=[0],
    cancel_buttons=[1],
    up_buttons=[],
    down_buttons=[],
    left_buttons=[],
    right_buttons=[],
    axes=[(0, 1, False, False)],
    hats=[]
)


def get_joystick_mapping(joystick: Joystick):
    guid = joystick.get_guid()
    if guid in joystick_mappings:
        return joystick_mappings[guid]
    # on the monkey arcade the second joystick is inversed on the left/right
    if guid == "03000000c0160000e105000000000000" and joystick.get_instance_id() == 0:
        return JoystickMapping(
            ok_buttons=[0],
            cancel_buttons=[1],
            up_buttons=[],
            down_buttons=[],
            left_buttons=[],
            right_buttons=[],
            axes=[(0, 1, True, False)],
            hats=[]
        )
    return default_joystick_mapping


class JoystickAnalyzer:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Joystick Analyzer")

        # Set up the joystick
        pygame.joystick.init()

        self.my_joystick = None
        self.joystick_names = []

        # Enumerate joysticks
        for i in range(0, pygame.joystick.get_count()):
            self.joystick_names.append(pygame.joystick.Joystick(i).get_name())

        print(self.joystick_names)

        # By default, load the first available joystick.
        if len(self.joystick_names) > 0:
            self.my_joystick = pygame.joystick.Joystick(0)
            self.my_joystick.init()

        max_joy = max(self.my_joystick.get_numaxes(),
                      self.my_joystick.get_numbuttons(),
                      self.my_joystick.get_numhats())

        self.screen = pygame.display.set_mode((max_joy * 30 + 10, 180))

        self.font = pygame.font.SysFont("Courier", 20)

    # A couple of joystick functions...
    def check_axis(self, p_axis):
        if self.my_joystick:
            if p_axis & self.my_joystick.get_numaxes():
                return self.my_joystick.get_axis(p_axis)

        return 0

    def check_button(self, p_button):
        if self.my_joystick:
            if p_button & self.my_joystick.get_numbuttons():
                return self.my_joystick.get_button(p_button)

        return False

    def check_hat(self, p_hat):
        if self.my_joystick:
            if p_hat & self.my_joystick.get_numhats():
                return self.my_joystick.get_hat(p_hat)

        return 0, 0

    def draw_text(self, text, x, y, color):
        surface = self.font.render(text, True, color, (0, 0, 0))
        surface.set_colorkey((0, 0, 0))

        self.screen.blit(surface, (x, y))

    def center_text(self, text, x, y, color):
        surface = self.font.render(text, True, color, (0, 0, 0))
        surface.set_colorkey((0, 0, 0))

        self.screen.blit(surface, (x - surface.get_width() / 2,
                                   y - surface.get_height() / 2))

    def main(self):
        while True:
            g_keys = pygame.event.get()

            self.screen.fill(0)

            for event in g_keys:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.display.quit()
                    return

                elif event.type == pygame.QUIT:
                    pygame.display.quit()
                    return

            self.draw_text("%s" % self.joystick_names[0],
                           5, 5, (0, 255, 0))

            self.draw_text("Axes (%d)" % self.my_joystick.get_numaxes(),
                           5, 25, (255, 255, 255))

            for i in range(0, self.my_joystick.get_numaxes()):
                if math.fabs(self.my_joystick.get_axis(i)) > 0.1:
                    pygame.draw.circle(self.screen, (0, 0, 200),
                                       (20 + (i * 30), 60), 10, 0)
                else:
                    pygame.draw.circle(self.screen, (255, 0, 0),
                                       (20 + (i * 30), 60), 10, 0)

                self.center_text("%d" % i, 20 + (i * 30), 60, (255, 255, 255))

            self.draw_text("Buttons (%d)" % self.my_joystick.get_numbuttons(),
                           5, 75, (255, 255, 255))

            for i in range(0, self.my_joystick.get_numbuttons()):
                if self.my_joystick.get_button(i):
                    pygame.draw.circle(self.screen, (0, 0, 200),
                                       (20 + (i * 30), 110), 10, 0)
                else:
                    pygame.draw.circle(self.screen, (255, 0, 0),
                                       (20 + (i * 30), 110), 10, 0)

                self.center_text("%d" % i, 20 + (i * 30), 110, (255, 255, 255))

            self.draw_text("POV Hats (%d)" % self.my_joystick.get_numhats(),
                           5, 125, (255, 255, 255))

            for i in range(0, self.my_joystick.get_numhats()):
                if self.my_joystick.get_hat(i) != (0, 0):
                    pygame.draw.circle(self.screen, (0, 0, 200),
                                       (20 + (i * 30), 160), 10, 0)
                else:
                    pygame.draw.circle(self.screen, (255, 0, 0),
                                       (20 + (i * 30), 160), 10, 0)

                self.center_text("%d" % i, 20 + (i * 30), 160, (255, 255, 255))

            pygame.display.flip()


if __name__ == "__main__":
    joystickAnalyzer = JoystickAnalyzer()
    joystickAnalyzer.main()
