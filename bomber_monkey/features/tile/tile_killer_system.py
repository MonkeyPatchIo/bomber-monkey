from typing import Any, Callable

from bomber_monkey.features.board.board import Tiles
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.tile.tile_killer import TileKiller
from python_ecs.ecs import System, Simulator


class TileKillerSystem(System):

    def __init__(self, spawner: Callable[[RigidBody], Any]):
        super().__init__([TileKiller, RigidBody])
        self.spawner = spawner

    def update(self, sim: Simulator, dt: float, killer: TileKiller, body: RigidBody) -> None:
        cell = sim.context.board.by_pixel(body.pos)
        if cell.tile == killer.tile:
            cell.tile = Tiles.EMPTY
            if self.spawner:
                self.spawner(body)
