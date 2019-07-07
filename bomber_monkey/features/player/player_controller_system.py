import pygame as pg

from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.player.player_controller import PlayerController
from python_ecs.ecs import System, Simulator


class PlayerControllerSystem(System):
    treshold = .5

    def __init__(self):
        super().__init__([RigidBody, PlayerController])

    def update(self, sim: Simulator, dt: float, body: RigidBody, player_controller: PlayerController):
        keys = pg.key.get_pressed()
        for k, action in player_controller.actions.items():
            if k and keys[k]:
                action(body)

        joystick = player_controller.joystick
        if joystick:
            if joystick.get_numaxes() >= 2:
                axis_0 = joystick.get_axis(0) * (-1 if player_controller.axis_x else 1)
                axis_1 = joystick.get_axis(1) * (-1 if player_controller.axis_y else 1)
                self.handle_axis(body, player_controller, axis_0, axis_1)

            if joystick.get_numhats() >= 1:
                axis_0, axis_1 = joystick.get_hat(0)
                axis_0 *= (-1 if player_controller.axis_x else 1)
                axis_1 *= (-1 if player_controller.axis_y else 1)

                self.handle_axis(body, player_controller, axis_0, -axis_1)

            for _ in range(0, joystick.get_numbuttons()):
                if joystick.get_button(_):
                    player_controller.special_action(body)

    def handle_axis(self, body: RigidBody, player_controller: PlayerController, axis_0, axis_1):
        if axis_0 < -PlayerControllerSystem.treshold:
            player_controller.left_action(body)
        if axis_0 > PlayerControllerSystem.treshold:
            player_controller.right_action(body)

        if axis_1 < -PlayerControllerSystem.treshold:
            player_controller.up_action(body)
        if axis_1 > PlayerControllerSystem.treshold:
            player_controller.down_action(body)
