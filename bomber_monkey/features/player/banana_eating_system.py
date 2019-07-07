from bomber_monkey.features.banana.banana import Banana
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.player.player import Player
from bomber_monkey.game_factory import GameFactory
from bomber_monkey.utils.collision_detector import detect_collision
from python_ecs.ecs import System, Simulator


class BananaEatingSystem(System):

    def __init__(self, factory: GameFactory):
        super().__init__([Player, RigidBody])
        self.factory = factory

    def update(self, sim: Simulator, dt: float, player: Player, body: RigidBody) -> None:
        cell = self.factory.board.by_pixel(body.pos)

        for _ in filter(None, [cell, cell.right(), cell.left(), cell.down(), cell.up()]):
            for banana in _.get(Banana):
                banana_body: RigidBody = banana.get(RigidBody)
                if detect_collision(body, banana_body):
                    banana.destroy()
                    player.power = min(player.power + 1, 10)
