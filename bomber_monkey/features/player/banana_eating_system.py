from bomber_monkey.features.banana.banana import Banana
from bomber_monkey.features.bomb.bomb import Bomb
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.physics.shape import Shape
from bomber_monkey.features.player.player import Player
from bomber_monkey.game_state import GameState
from bomber_monkey.utils.collision_detector import detect_collision
from python_ecs.ecs import System, sim


class BananaEatingSystem(System):

    def __init__(self, game_state: GameState):
        super().__init__([Banana, RigidBody, Shape])
        self.game_state = game_state

    def update(self, banana: Banana, body: RigidBody, shape: Shape) -> None:
        for player in self.game_state.players:
            player_body: RigidBody = player.get(RigidBody)
            player_shape: Shape = player.get(Shape)
            player_c: Player = player.get(Player)

            if detect_collision(player_body, player_shape, body, shape):
                sim.get(banana.eid).destroy()
                player_c.power += 1
