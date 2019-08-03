import os

from bomber_monkey.features.board.board import Board
from bomber_monkey.features.player.player_slot import PlayerSlot
from bomber_monkey.utils.graphics_cache import GraphicsCache
from bomber_monkey.utils.vector import Vector


class GameConfig(object):
    def __init__(self):
        self.resources_path = 'resources/'

        self.banana_drop_rate = .18
        self.grid_size = Vector.create(17, 11)
        self.tile_size = Vector.create(64, 64)
        self.playground_offset = Vector.create(0, 90)
        self.player_accel = 2000
        self.player_max_speed = 200
        self.player_death_duration = 1
        self.friction_ratio = 0.2
        self.bomb_duration = 2.0
        self.bomb_power = 1
        self.bomb_drop_rate = .35
        self.bomb_explosion_propagation_time = 1
        self.explosion_duration = 5
        self.winning_score = 3
        self.graphics_cache = GraphicsCache()

        self.JOYSTICK_ESCAPE_BUTTON = 2

        self.PLAYER_NUMBER = 4  # max 4
        self.PLAYER_PERMUTATION = [1, 0, 2, 3]
        self.INVERT_X = [True, False, False]
        self.INVERT_Y = [False, False, False]

        self.MAX_FPS = 60

        self.DEBUG_MODE = False

    def player_slots(self, board: Board):
        return [
            PlayerSlot(
                player_id=0,
                start_pos=Vector.create(1, 1),
                color=(255, 0, 0),
                score_pos=(5, 3)
            ),

            PlayerSlot(
                player_id=1,
                start_pos=Vector.create(board.width - 2, board.height - 2),
                color=(0, 0, 255),
                score_pos=(self.pixel_size.x - 45, 3 + 45)
            ),
            PlayerSlot(
                player_id=2,
                start_pos=Vector.create(1, board.height - 2),
                color=(0, 255, 0),
                score_pos=(5, 3 + 45)
            ),
            PlayerSlot(
                player_id=3,
                start_pos=Vector.create(board.width - 2, 1),
                color=(255, 255, 0),
                score_pos=(self.pixel_size.x - 45, 3)
            )
        ]

    def media_path(self, path):
        return os.path.join(self.resources_path, path)

    @property
    def pixel_size(self) -> Vector:
        return self.tile_size * self.grid_size + self.playground_offset
