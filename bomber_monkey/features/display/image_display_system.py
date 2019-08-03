from bomber_monkey.features.display.image import Image
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.game_config import GameConfig
from python_ecs.ecs import System, Simulator


class ImageDisplaySystem(System):
    def __init__(self, conf: GameConfig, screen):
        super().__init__([RigidBody, Image])
        self.conf = conf
        self.graphics_cache = self.conf.graphics_cache
        self.screen = screen
        self.images = {}

    def update(self, sim: Simulator, dt: float, body: RigidBody, image: Image) -> None:
        pos = body.pos
        if image.display_size:
            pos = body.pos - image.display_size // 2
        pos += self.conf.playground_offset

        graphic = self.graphics_cache.get_image(image)
        self.screen.blit(graphic, pos.data)
