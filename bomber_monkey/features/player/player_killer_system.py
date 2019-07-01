from bomber_monkey.features.player.player_killer import PlayerKiller
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.physics.shape import Shape
from bomber_monkey.states.in_game import GameState
from bomber_monkey.utils.collision_detector import detect_collision
from python_ecs.ecs import System


class PlayerKillerSystem(System):

    def __init__(self, game_state: GameState):
        super().__init__([PlayerKiller, RigidBody, Shape])
        self.game_state = game_state

    def update(self, dt: float, killer: PlayerKiller, body: RigidBody, shape: Shape) -> None:
        for player in self.game_state.players:
            player_body: RigidBody = player.get(RigidBody)
            player_shape: Shape = player.get(Shape)
            if detect_collision(player_body, player_shape, body, shape):
                player.destroy()
