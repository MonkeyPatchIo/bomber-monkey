import os

import pygame_menu

from bomber_monkey.utils.graphics_cache import GraphicsCache
from bomber_monkey.utils.vector import Vector

GAME_FONT = pygame_menu.font.FONT_8BIT

BLUE_MONKEY_COLOR = (0, 176, 240)
WHITE_COLOR = (255, 255, 255)
GREY_COLOR = (180, 180, 180)
BLACK_COLOR = (0, 0, 0)
ORANGE_COLOR = (229, 157, 68)
RED_COLOR = (255, 0, 0)
GREEN_COLOR = (0, 255, 0)

MENU_FONT_SIZE = 50
MENU_THEME = pygame_menu.themes.Theme(
    title_font=GAME_FONT,
    title_font_size=MENU_FONT_SIZE,
    title_font_color=BLUE_MONKEY_COLOR,
    widget_font=GAME_FONT,
    widget_font_size=MENU_FONT_SIZE,
    background_color=BLACK_COLOR,
)


class GameConfig(object):
    def __init__(self):
        self.resources_path = 'resources/'

        self.item_rates = {
            'None': 5,
            'Banana': 4,
            'PhpItem': 1,
            'RustItem': 3,
            'JavaItem': 2,
            'Html5Item': 1
        }
        self.immunity_duration = 10.0
        self.grid_size = Vector.create(17, 11)
        self.tile_size = Vector.create(64, 64)
        self.playground_offset = Vector.create(0, 90)
        self.max_pos_diff = Vector.create(32, 32)
        self.player_accel = 2000
        self.player_max_speed = 200
        self.speed_up = 1.2
        self.player_death_duration = 1.0
        self.friction_ratio = 0.2
        self.bomb_duration = 2.0
        self.bomb_power = 1
        self.bomb_drop_rate = .35
        self.bomb_explosion_propagation_time = 0.0001
        self.explosion_duration = 0.4
        self.crushing_wait_duration = 0.5
        self.winning_score = 3
        self.game_startup_delay = 3
        self.score_board_min_display_time = 1
        self.graphics_cache = GraphicsCache()
        self.fullscreen = False

        self.JOYSTICK_ESCAPE_BUTTON = 2

        self.MAX_FPS = 60

        self.DEBUG_MODE = False

    def media_path(self, path):
        return os.path.join(self.resources_path, path)

    @property
    def pixel_size(self) -> Vector:
        return self.tile_size * self.grid_size + self.playground_offset
