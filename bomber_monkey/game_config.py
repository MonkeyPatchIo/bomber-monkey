from bomber_monkey.utils.image_loader import ImageLoader
from bomber_monkey.utils.vector import Vector


class GameConfig(object):
    def __init__(self):
        self.banana_drop_rate = .15
        self.grid_size = Vector.create(17, 11)
        self.tile_size = Vector.create(64, 64)
        self.playground_offset = Vector.create(0, 90)
        self.bomb_duration = 2.0
        self.bomb_power = 1
        self.bomb_drop_rate = .35
        self.explosion_duration = .2
        self.winning_score = 3
        self.debug_fps = False
        self.image_loader = ImageLoader()

        self.JOYSTICK_ESCAPE_BUTTON = 2

        self.PLAYER_NUMBER = 4  # max 4
        self.PLAYER_PERMUTATION = [1, 0, 2, 3]
        self.INVERT_X = [True, False, False]
        self.INVERT_Y = [False, False, False]

    @property
    def pixel_size(self) -> Vector:
        return self.tile_size * self.grid_size + self.playground_offset
