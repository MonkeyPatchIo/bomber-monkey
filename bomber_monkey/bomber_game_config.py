import time
from typing import Dict

import pygame
from pygame.surface import Surface

from bomber_monkey.features.board.board import Board, random_blocks, Tiles, fill_border, clear_corners
from bomber_monkey.features.bomb.bomb_explosion import BombExplosion
from bomber_monkey.features.bomb.player_killer import PlayerKiller
from bomber_monkey.features.display.image import Image
from bomber_monkey.features.lifetime.lifetime import Lifetime
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.physics.shape import Shape
from bomber_monkey.features.player.player import Player
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import sim, Entity


class ImageLoader(object):
    def __init__(self):
        self.graphics: Dict[Image, Surface] = {}

    def __getitem__(self, image):
        graphic = self.graphics.get(image, None)
        if graphic is None:
            graphic = pygame.image.load(image.path)
            if image.size:
                graphic = pygame.transform.scale(graphic, image.size.data)
            self.graphics[image] = graphic
        return graphic

class BomberGameConfig(object):
    def __init__(self):
        self.grid_size = Vector.create(20, 12)
        self.tile_size = Vector.create(64, 64)
        self.bomb_duration = 2.5
        self.explosion_duration = 1
        self._board: Board = None
        self._players: list[Entity] = []
        self.image_loader = ImageLoader()

    @property
    def pixel_size(self) -> Vector:
        return self.tile_size.data * self.grid_size.data

    def create_player(self, grid_pos: Vector):
        pos = grid_pos * self.tile_size + self.tile_size // 2

        player = sim.create(
            RigidBody(
                pos=pos
            ),
            Shape(self.tile_size),
            Image('resources/monkey.png'),
            Player(len(self._players) + 1)
        )
        self._players.append(player)
        return player

    def _on_destroy_player(self, entity: Entity):
        player: Player = entity.get(Player)
        if player:
            self._players.remove(entity)

    @property
    def players(self) -> list:
        return self._players

    def create_explosion(self, pos: Vector):
        return sim.create(
            RigidBody(pos=pos),
            Shape(self.tile_size),
            Image('resources/fire.png'),
            Lifetime(self.explosion_duration),
            PlayerKiller()
        )

    def create_board(self):
        board = Board(tile_size=self.tile_size, grid_size=self.grid_size)
        sim.on_create.append(board.on_create)
        sim.on_destroy.append(board.on_destroy)
        sim.on_destroy.append(self._on_destroy_player)

        random_blocks(board, Tiles.WALL, .2)
        random_blocks(board, Tiles.BLOCK, .5)
        clear_corners(board)
        fill_border(board, Tiles.WALL)
        self._board = board
        self._players = []

        return sim.create(board)

    @property
    def board(self) -> Board:
        return self._board

    def create_bomb(self, avatar: Entity):
        global last_creation
        now = time.time()
        if now - last_creation > .5:
            last_creation = now
            board: Board = self.board
            body: RigidBody = avatar.get(RigidBody)

            bomb_pos = board.by_pixel(body.pos).center
            sim.create(
                RigidBody(
                    pos=bomb_pos
                ),
                Shape(self.tile_size),
                Image('resources/bomb.png'),
                Lifetime(self.bomb_duration),
                BombExplosion(3)
            )


last_creation = time.time()
