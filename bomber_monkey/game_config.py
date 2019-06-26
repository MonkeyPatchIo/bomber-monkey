
from bomber_monkey.utils.image_loader import ImageLoader
from bomber_monkey.utils.vector import Vector


class GameConfig(object):
    def __init__(self):
        self.grid_size = Vector.create(20, 12)
        self.tile_size = Vector.create(64, 64)
        self.playground_offset = Vector.create(0, 60)
        self.bomb_duration = 2.5
        self.bomb_power = 3
        self.bomb_drop_rate = 0.5
        self.explosion_duration = .25
        self.winning_score = 5
        self.image_loader = ImageLoader()

    @property
    def pixel_size(self) -> Vector:
        return self.tile_size * self.grid_size + self.playground_offset
