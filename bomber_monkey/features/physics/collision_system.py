import numpy as np

from bomber_monkey.features.board.board import Tiles, Cell, Board
from bomber_monkey.features.physics.physic_system import PhysicSystem
from bomber_monkey.features.physics.rigid_body import RigidBody
from python_ecs.ecs import System, Simulator


class PlayerCollisionSystem(System):
    def __init__(self, board: Board):
        super().__init__([RigidBody])
        self.board = board

    def update(self, sim: Simulator, dt: float, body: RigidBody) -> None:
        def stop_x():
            body.speed.x = 0
            body.accel.x = 0

        def stop_y():
            body.speed.y = 0
            body.accel.y = 0

        cell = self.board.by_pixel(body.pos)

        if not cell:
            return

        def is_blocker(cell: Cell, next_cell: Cell):
            wall_blocker = next_cell.tile in (Tiles.BLOCK, Tiles.WALL)
            bomb_blocker = next_cell.has_bomb and (cell.grid != next_cell.grid)
            return wall_blocker or bomb_blocker

        next_pos, next_speed = PhysicSystem.next_state(body, dt)

        cell_x = cell.right() if next_speed.x > 0 else cell.left()

        SHAPE_COEF = 1
        if cell_x:
            in_range_x = abs(next_pos.x - cell_x.center.x) < self.board.tile_size.x * SHAPE_COEF
            if in_range_x and is_blocker(cell, cell_x):
                stop_x()

        cell_y = cell.down() if next_speed.y > 0 else cell.up()
        if cell_y:
            in_range_y = abs(next_pos.y - cell_y.center.y) < self.board.tile_size.y * SHAPE_COEF
            if in_range_y and is_blocker(cell, cell_y):
                stop_y()

        next_cell = self.board.by_pixel(next_pos)
        if next_cell:
            in_range = np.linalg.norm(next_pos.data - next_cell.center.data) < self.board.tile_size.y * SHAPE_COEF
            if in_range and is_blocker(cell, next_cell):
                stop_x()
                stop_y()
