import sys

import pygame as pg

from bomber_monkey.features.board.board import Board
from bomber_monkey.features.board.board_display_system import BoardDisplaySystem
from bomber_monkey.features.display.background import Background
from bomber_monkey.features.display.background_system import BackgroundSystem
from bomber_monkey.features.display.display_system import DisplaySystem
from bomber_monkey.features.display.image import Image
from bomber_monkey.features.keyboard.keyboard_system import KeyboardSystem
from bomber_monkey.features.keyboard.keymap import Keymap
from bomber_monkey.features.move.move_system import MoveSystem
from bomber_monkey.features.move.position import Position
from bomber_monkey.features.move.speed import Speed
from bomber_monkey.features.physics.friction_system import FrictionSystem
from python_ecs.ecs import sim, Entity


def main():
    # init pygame
    screen = init_pygame(1400, 900)

    # init simulation (ECS)
    sim.reset_systems([
        KeyboardSystem(),
        MoveSystem(),
        FrictionSystem(0.995),
        BackgroundSystem(screen),
        BoardDisplaySystem(screen, (32, 32)),
        DisplaySystem(screen),
    ])
    # create background
    sim.create(Background(0, 0, 0))

    board = sim.create(Board(10, 10))

    # create avatar
    avatar = sim.create(
        Position(10, 10),
        Speed(0, 0),
        Image('resources/bomb.png')
    )
    # create heyboard handlers
    sim.create(Keymap({
        #    https://www.pygame.org/docs/ref/key.html
        pg.K_DOWN: mover(avatar, 0, 1),
        pg.K_UP: mover(avatar, 0, -1),
        pg.K_LEFT: mover(avatar, -1, 0),
        pg.K_RIGHT: mover(avatar, 1, 0),
        pg.K_ESCAPE: lambda x: sys.exit()
    }))

    run_game(sim)


def mover(obj: Entity, dx: int, dy: int):
    def move(event):
        if event.type == pg.KEYDOWN:
            speed = obj.get(Speed)
            speed.x += dx * .05
            speed.y += dy * .05

    return move


def init_pygame(screen_width, screen_height):
    pg.init()
    pg.key.set_repeat(1)
    # load and set the logo
    logo = pg.image.load("resources/bomb.png")
    pg.display.set_icon(logo)
    pg.display.set_caption('my game')
    screen = pg.display.set_mode((screen_width, screen_height))
    return screen


def run_game(sim):
    while True:
        sim.update()
        pg.display.flip()


if __name__ == "__main__":
    main()
