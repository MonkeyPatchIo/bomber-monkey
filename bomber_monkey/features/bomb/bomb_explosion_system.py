import time

from bomber_monkey.features.board.board import Tiles, Cell
from bomber_monkey.features.bomb.bomb import Bomb
from bomber_monkey.features.lifetime.lifetime import Lifetime
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.game_state import GameState
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import System, sim


class BombExplosionSystem(System):

    def __init__(self, game_state: GameState):
        super().__init__([Bomb, RigidBody, Lifetime])
        self.game_state = game_state

    def update(self, explosion: Bomb, body: RigidBody, lifetime: Lifetime) -> None:
        now = time.time()

        if not explosion.is_done and now > lifetime.dead_time:
            explosion.is_done = True
            sim.get(explosion.eid).destroy()
            bomb_cell: Cell = self.game_state.board.by_pixel(body.pos)
            self.game_state.create_explosion(bomb_cell.center)
            directions = [Vector.create(x, y) for x, y in [(0, -1), (1, 0), (0, 1), (-1, 0)]]
            for direction in directions:
                for i in range(1, explosion.explosion_size + 1):
                    cell: Cell = bomb_cell.move(direction * i)
                    if cell is None or cell.tile == Tiles.WALL:
                        break
                    self.game_state.create_explosion(cell.center)
                    if cell.tile == Tiles.BLOCK:
                        cell.tile = Tiles.EMPTY
                        break
