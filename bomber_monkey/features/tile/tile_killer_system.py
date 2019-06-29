from typing import Any, Callable

from bomber_monkey.features.board.board import Tiles, Board
from bomber_monkey.features.tile.tile_killer import TileKiller
from bomber_monkey.features.physics.rigid_body import RigidBody
from python_ecs.ecs import System


class WallExplosionSystem(System):

    def __init__(self, board: Board, factory: Callable[[RigidBody], Any]):
        super().__init__([TileKiller, RigidBody])
        self.board = board
        self.factory = factory

    def update(self, killer: TileKiller, body: RigidBody) -> None:
        cell = self.board.by_pixel(body.pos)
        if cell.tile == killer.tile:
            cell.tile = Tiles.EMPTY
            if self.factory:
                self.factory(body)
