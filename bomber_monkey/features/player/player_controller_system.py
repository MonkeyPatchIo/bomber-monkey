import pygame as pg

from bomber_monkey.game_state import GameState
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.player.player_controller import PlayerController
from python_ecs.ecs import System


class PlayerControllerSystem(System):
    def __init__(self, state: GameState):
        super().__init__([RigidBody, PlayerController])
        self.state = state

    def update(self, body: RigidBody, player_controller: PlayerController):
        keys = pg.key.get_pressed()
        for k, action in player_controller.actions.items():
            if keys[k]:
                action(self.state, body)
