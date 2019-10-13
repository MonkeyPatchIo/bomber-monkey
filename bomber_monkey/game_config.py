import os

import pygameMenu

from bomber_monkey.utils.graphics_cache import GraphicsCache
from bomber_monkey.utils.vector import Vector

GAME_FONT = pygameMenu.font.FONT_8BIT

BLUE_MONKEY_COLOR = (0, 176, 240)
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
ORANGE_COLOR = (229, 157, 68)
RED_COLOR = (255, 0, 0)
GREEN_COLOR = (0, 255, 0)


class GameConfig(object):
    def __init__(self):
        self.resources_path = 'resources/'

        self.banana_drop_rate = .18
        self.grid_size = Vector.create(17, 11)
        self.tile_size = Vector.create(64, 64)
        self.playground_offset = Vector.create(0, 90)
        self.max_pos_diff = Vector.create(32, 32)
        self.player_accel = 2000
        self.player_max_speed = 200
        self.player_death_duration = 1
        self.friction_ratio = 0.2
        self.bomb_duration = 2.0
        self.bomb_power = 1
        self.bomb_drop_rate = .35
        self.bomb_explosion_propagation_time = .12
        self.explosion_duration = 2.0
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
