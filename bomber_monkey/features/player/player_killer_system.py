from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.physics.shape import Shape
from bomber_monkey.features.player.player_killer import PlayerKiller
from bomber_monkey.game_factory import GameFactory
from bomber_monkey.utils.collision_detector import detect_collision
from python_ecs.ecs import System


class PlayerKillerSystem(System):

    def __init__(self, factory: GameFactory):
        super().__init__([PlayerKiller, RigidBody])
        self.factory = factory

    def update(self, dt: float, killer: PlayerKiller, body: RigidBody) -> None:
        for player in self.factory.players:
            player_body: RigidBody = player.get(RigidBody)
            if detect_collision(player_body, body):
                player.destroy()
