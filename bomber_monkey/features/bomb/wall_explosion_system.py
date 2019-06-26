from bomber_monkey.features.board.board import Tiles, Board
from bomber_monkey.features.bomb.wall_killer import WallKiller
from bomber_monkey.features.physics.rigid_body import RigidBody
from python_ecs.ecs import System


class WallExplosionSystem(System):

    def __init__(self, board: Board):
        super().__init__([WallKiller, RigidBody])
        self.board = board

    def update(self, _killer: WallKiller, body: RigidBody) -> None:
        cell = self.board.by_pixel(body.pos)
        if cell.tile == Tiles.BLOCK:
            cell.tile = Tiles.EMPTY
