from bomber_monkey.features.banana.banana import Banana
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.player.player import Player
from bomber_monkey.game_factory import GameFactory
from bomber_monkey.utils.collision_detector import detect_collision
from python_ecs.ecs import System


class BananaEatingSystem(System):

    def __init__(self, factory: GameFactory):
        super().__init__([Banana, RigidBody])
        self.factory = factory

    def update(self, dt: float, banana: Banana, body: RigidBody) -> None:
        for player in self.factory.players:
            player_body: RigidBody = player.get(RigidBody)
            player_c: Player = player.get(Player)

            if detect_collision(player_body, body):
                banana.entity().destroy()
                player_c.power += 1
