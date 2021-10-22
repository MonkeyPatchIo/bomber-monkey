from typing import Tuple, Optional, List

import numpy as np

from bomber_monkey.features.board.board import Tiles, Cell, Board
from bomber_monkey.features.physics.physic_system import PlayerCollisionPhysic
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.game_config import GameConfig
from bomber_monkey.utils.vector import sign, Vector
from python_ecs.ecs import Simulator

EPSILON = 0.1
SLIDE_FRICTION = 0.8


class SimplePlayerCollisionPhysic(PlayerCollisionPhysic):

    def update(self, sim: Simulator, dt: float, body: RigidBody, next_pos: Vector, next_speed: Vector
               ) -> Tuple[Vector, Vector, List[Cell]]:
        board: Board = sim.context.board

        def stop_x():
            next_speed.x = 0
            next_pos.x = body.pos.x

        def stop_y():
            next_speed.y = 0
            next_pos.y = body.pos.y

        cell = board.by_pixel(body.pos)

        if not cell:
            return next_pos, next_speed, []

        def is_blocker(c: Cell, next_c: Cell):
            wall_blocker = c.tile in (Tiles.BLOCK, Tiles.WALL)
            bomb_blocker = c.has_bomb and (cell.grid != next_c.grid)
            return wall_blocker or bomb_blocker

        cell_x = cell.right() if next_speed.x > 0 else cell.left()

        SHAPE_COEF = 1
        if cell_x:
            in_range_x = abs(next_pos.x - cell_x.center.x) < board.tile_size.x * SHAPE_COEF
            if in_range_x and is_blocker(cell, cell_x):
                stop_x()

        cell_y = cell.down() if next_speed.y > 0 else cell.up()
        if cell_y:
            in_range_y = abs(next_pos.y - cell_y.center.y) < board.tile_size.y * SHAPE_COEF
            if in_range_y and is_blocker(cell, cell_y):
                stop_y()

        next_cell = board.by_pixel(next_pos)
        if next_cell:
            in_range = np.linalg.norm(next_pos.data - next_cell.center.data) < board.tile_size.y * SHAPE_COEF
            if in_range and is_blocker(cell, next_cell):
                stop_x()
                stop_y()

        return next_pos, next_speed, []


class PlayerCollisionWithDTPhysic(PlayerCollisionPhysic):

    def update(self, sim: Simulator, dt: float, body: RigidBody, next_pos: Vector, next_speed: Vector
               ) -> Tuple[Vector, Vector, List[Cell]]:
        board: Board = sim.context.board
        conf: GameConfig = sim.context.conf

        cell = board.by_pixel(body.pos)

        if not cell:
            return next_pos, next_speed, []

        half_rigid_shape = body.shape.data / 2
        half_tile_size = board.tile_size / 2

        def is_blocker(c: Cell, next_c: Cell):
            wall_blocker = next_c.tile in (Tiles.BLOCK, Tiles.WALL)
            bomb_blocker = next_c.has_bomb and (c.grid != next_c.grid)
            return wall_blocker or bomb_blocker

        def check_next(axe: int, next_cell):
            if next_cell and is_blocker(cell, next_cell):
                speed_sign = sign(next_speed.data[axe])
                overlap = next_pos.data[axe] + speed_sign * half_rigid_shape.data[axe] \
                    - (next_cell.center.data[axe] - speed_sign * half_tile_size.data[axe])
                if abs(overlap) > EPSILON and sign(overlap) == speed_sign:
                    next_speed.data[axe] = 0
                    next_pos.data[axe] -= overlap
                    return next_cell
            return None

        moving_x = abs(next_speed.x) > EPSILON
        moving_y = abs(next_speed.y) > EPSILON

        blocking_cell_x: Optional[Cell] = None
        if moving_x:
            next_cell_x = cell.right() if next_speed.x > 0 else cell.left()
            # check for blocking from a block in front
            blocking_cell_x = check_next(0, next_cell_x)
            # check for blocking from a block on the side up
            if blocking_cell_x is None and body.pos.y - half_rigid_shape.y - (
                    cell.center.y - half_tile_size.y) < -EPSILON:
                blocking_cell_x = check_next(0, next_cell_x.up())
            # check for blocking from a block on the side down
            if blocking_cell_x is None and body.pos.y + half_rigid_shape.y - (
                    cell.center.y + half_tile_size.y) > EPSILON:
                blocking_cell_x = check_next(0, next_cell_x.down())

        blocking_cell_y: Optional[Cell] = None
        if moving_y:
            next_cell_y = cell.down() if next_speed.y > 0 else cell.up()
            # check for blocking from a block in front
            blocking_cell_y = check_next(1, next_cell_y)
            # check for blocking from a block on the side left
            if blocking_cell_y is None and body.pos.x + half_rigid_shape.x - (
                    cell.center.x + half_tile_size.x) > EPSILON:
                blocking_cell_y = check_next(1, next_cell_y.right())
            # check for blocking from a block on the side right
            if blocking_cell_y is None and body.pos.x - half_rigid_shape.x - (
                    cell.center.x - half_tile_size.x) < -EPSILON:
                blocking_cell_y = check_next(1, next_cell_y.left())

        # check if we can slide off the blocking cell
        if blocking_cell_x is not None and blocking_cell_y is None and not moving_y:
            offset = body.pos.y - blocking_cell_x.center.y
            if abs(offset) > EPSILON:
                slide_cell = blocking_cell_x.down() if offset > 0 else blocking_cell_x.up()
                if not is_blocker(cell, slide_cell):
                    next_speed.y = sign(offset)  # to continue to animate
                    slide = max(2, min(half_tile_size.y + half_rigid_shape.y - abs(offset),
                                       conf.player_max_speed * SLIDE_FRICTION * dt))
                    next_pos.y += sign(offset) * slide
        elif blocking_cell_y is not None and blocking_cell_x is None and not moving_x:
            offset = body.pos.x - blocking_cell_y.center.x
            if abs(offset) > EPSILON:
                slide_cell = blocking_cell_y.right() if offset > 0 else blocking_cell_y.left()
                if not is_blocker(cell, slide_cell):
                    next_speed.x = sign(offset)  # to continue to animate
                    slide = max(2, min(half_tile_size.x + half_rigid_shape.x - abs(offset),
                                       conf.player_max_speed * SLIDE_FRICTION * dt))
                    next_pos.x += sign(offset) * slide

        return next_pos, next_speed, [c for c in [blocking_cell_x, blocking_cell_y] if c is not None]
