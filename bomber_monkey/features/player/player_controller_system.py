import pygame as pg

from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.player.player_controller import PlayerController
from python_ecs.ecs import System


class PlayerControllerSystem(System):
    treshold = .15

    def __init__(self, ):
        super().__init__([RigidBody, PlayerController])

    def update(self, dt: float, body: RigidBody, player_controller: PlayerController):
        keys = pg.key.get_pressed()
        for k, action in player_controller.actions.items():
            if keys[k]:
                action(body)

        joystick = player_controller.joystick
        if joystick:
            axis_0 = joystick.get_axis(0)
            axis_1 = joystick.get_axis(1)

            if axis_0 < PlayerControllerSystem.treshold:
                player_controller.left_action(body)
            elif axis_0 > PlayerControllerSystem.treshold:
                player_controller.right_action(body)

            if axis_1 < PlayerControllerSystem.treshold:
                player_controller.down_action(body)
            elif axis_1 > PlayerControllerSystem.treshold:
                player_controller.up_action(body)

            if joystick.get_button(0):
                player_controller.special_action(body)
