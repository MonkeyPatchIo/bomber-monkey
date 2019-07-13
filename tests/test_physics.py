from bomber_monkey.features.board.board import Board, Tiles
from bomber_monkey.features.physics.collision_physic import PlayerCollisionWithDTPhysic
from bomber_monkey.features.physics.physic_system import PhysicSystem
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.physics.shape import Shape
from bomber_monkey.game_config import GameConfig
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import Simulator


board_size = Vector.create(5, 5)
tile_size = Vector.create(10, 10)
player_size = Vector.create(8, 8)
no_accel = Vector.create(0, 0)
player_shape = Shape(player_size)


class Context(object):
    def __init__(self, conf: GameConfig, board: Board):
        self.conf = conf
        self.board = board


def create_env():
    board = Board(
        board_size,
        tile_size
    )
    conf = GameConfig()
    conf.friction_ratio = 1
    sim = Simulator(Context(conf, board))
    sim.on_create.append(board.on_create)
    physics = PhysicSystem(PlayerCollisionWithDTPhysic())
    return board, conf, sim, physics


def create_body(sim: Simulator, pos: Vector, speed: Vector):
    body = RigidBody(
        pos=pos,
        speed=speed,
        accel=no_accel,
        shape=player_shape
    )
    sim.create(body)
    sim.update()
    return body


def test_physic_system():
    board, conf, sim, physics = create_env()
    conf.friction_ratio = 0.5
    body = create_body(
        sim,
        pos=Vector.create(5, 5),
        speed=Vector.create(20, 20),
    )
    dt = 1
    physics.update(sim, dt, body)

    assert body.speed == [10, 10]
    assert body.pos == [25, 25]


def test_player_collision():
    board, conf, sim, physics = create_env()
    dt = 1

    player_cell = board.by_grid(Vector.create(1, 1))
    player_cell.up().tile = Tiles.WALL
    player_cell.down().tile = Tiles.WALL
    player_cell.left().tile = Tiles.WALL
    player_cell.right().tile = Tiles.WALL

    # test blocked move right
    body = create_body(
        sim,
        pos=player_cell.center,
        speed=Vector.create(tile_size.x, 0),
    )
    physics.update(sim, dt, body)
    assert body.speed == [0, 0]
    assert body.pos == player_cell.center + Vector.create(1, 0)

    # test blocked move left
    body = create_body(
        sim,
        pos=player_cell.center,
        speed=Vector.create(-tile_size.x, 0),
    )
    physics.update(sim, dt, body)
    assert body.speed == [0, 0]
    assert body.pos == player_cell.center + Vector.create(-1, 0)

    # test blocked move up
    body = create_body(
        sim,
        pos=player_cell.center,
        speed=Vector.create(0, -tile_size.y),
    )
    physics.update(sim, dt, body)
    assert body.speed == [0, 0]
    assert body.pos == player_cell.center + Vector.create(0, -1)

    # test blocked move down
    body = create_body(
        sim,
        pos=player_cell.center,
        speed=Vector.create(0, tile_size.y),
    )
    physics.update(sim, dt, body)
    assert body.speed == [0, 0]
    assert body.pos == player_cell.center + Vector.create(0, 1)


def test_player_middle_no_collision():
    board, conf, sim, physics = create_env()
    dt = 1

    player_cell = board.by_grid(Vector.create(2, 2))
    player_cell.up().up().left().tile = Tiles.WALL
    player_cell.up().up().right().tile = Tiles.WALL
    player_cell.down().down().left().tile = Tiles.WALL
    player_cell.down().down().right().tile = Tiles.WALL
    player_cell.left().left().up().tile = Tiles.WALL
    player_cell.left().left().down().tile = Tiles.WALL
    player_cell.right().right().up().tile = Tiles.WALL
    player_cell.right().right().down().tile = Tiles.WALL

    # test non blocked move right in the middle
    body = create_body(
        sim,
        pos=player_cell.right().center,
        speed=Vector.create(tile_size.x, 0),
    )
    physics.update(sim, dt, body)
    assert body.speed.x == tile_size.x
    assert body.pos.x > player_cell.right().center.x

    # test non blocked move left in the middle
    body = create_body(
        sim,
        pos=player_cell.left().center,
        speed=Vector.create(-tile_size.x, 0),
    )
    physics.update(sim, dt, body)
    assert body.speed.x == -tile_size.x
    assert body.pos.x < player_cell.left().center.x

    # test non blocked move up in the middle
    body = create_body(
        sim,
        pos=player_cell.up().center,
        speed=Vector.create(0, -tile_size.y),
    )
    physics.update(sim, dt, body)
    assert body.speed.y == -tile_size.y
    assert body.pos.y < player_cell.up().center.y

    # test non blocked move down in the middle
    body = create_body(
        sim,
        pos=player_cell.down().center,
        speed=Vector.create(0, tile_size.y),
    )
    physics.update(sim, dt, body)
    assert body.speed.y == tile_size.y
    assert body.pos.y > player_cell.down().center.y


def test_player_side_collision():
    board, conf, sim, physics = create_env()
    dt = 1

    player_cell = board.by_grid(Vector.create(2, 2))
    player_cell.up().up().left().tile = Tiles.WALL
    player_cell.up().up().right().tile = Tiles.WALL
    player_cell.down().down().left().tile = Tiles.WALL
    player_cell.down().down().right().tile = Tiles.WALL
    player_cell.left().left().up().tile = Tiles.WALL
    player_cell.left().left().down().tile = Tiles.WALL
    player_cell.right().right().up().tile = Tiles.WALL
    player_cell.right().right().down().tile = Tiles.WALL

    # the offset to make the player shape above more than on grid
    offset = tile_size / 2 - player_size / 4

    # test blocked move right, because it is a little down
    pos = player_cell.right().center + Vector.create(0, offset.y)
    body = create_body(
        sim,
        pos=pos,
        speed=Vector.create(tile_size.x, 0),
    )
    physics.update(sim, dt, body)
    # assert blocked
    assert body.speed.x == 0
    assert body.pos.x == pos.x + 1
    # assert it is sliding
    assert body.speed.y < 0
    assert body.pos.y < pos.y

    # test blocked move right, because it is a little up
    pos = player_cell.right().center + Vector.create(0, -offset.y)
    body = create_body(
        sim,
        pos=pos,
        speed=Vector.create(tile_size.x, 0),
    )
    physics.update(sim, dt, body)
    # assert blocked
    assert body.speed.x == 0
    assert body.pos.x == pos.x + 1
    # assert it is sliding
    assert body.speed.y > 0
    assert body.pos.y > pos.y

    # test blocked move left, because it is a little down
    pos = player_cell.left().center + Vector.create(0, offset.y)
    body = create_body(
        sim,
        pos=pos,
        speed=Vector.create(-tile_size.x, 0),
    )
    physics.update(sim, dt, body)
    # assert blocked
    assert body.speed.x == 0
    assert body.pos.x == pos.x - 1
    # assert it is sliding
    assert body.speed.y < 0
    assert body.pos.y < pos.y

    # test blocked move left, because it is a little up
    pos = player_cell.left().center + Vector.create(0, -offset.y)
    body = create_body(
        sim,
        pos=pos,
        speed=Vector.create(-tile_size.x, 0),
    )
    physics.update(sim, dt, body)
    # assert blocked
    assert body.speed.x == 0
    assert body.pos.x == pos.x - 1
    # assert it is sliding
    assert body.speed.y > 0
    assert body.pos.y > pos.y

    # test blocked move up, because it is a little on the right
    pos = player_cell.up().center + Vector.create(offset.x, 0)
    body = create_body(
        sim,
        pos=pos,
        speed=Vector.create(0, -tile_size.y),
    )
    physics.update(sim, dt, body)
    # assert blocked
    assert body.speed.y == 0
    assert body.pos.y == pos.y - 1
    # assert it is sliding
    assert body.speed.x < 0
    assert body.pos.x < pos.x

    # test blocked move up, because it is a little on the left
    pos = player_cell.up().center + Vector.create(-offset.x, 0)
    body = create_body(
        sim,
        pos=pos,
        speed=Vector.create(0, -tile_size.y),
    )
    physics.update(sim, dt, body)
    # assert blocked
    assert body.speed.y == 0
    assert body.pos.y == pos.y - 1
    # assert it is sliding
    assert body.speed.x > 0
    assert body.pos.x > pos.x

    # test blocked move down, because it is a little on the right
    pos = player_cell.down().center + Vector.create(offset.x, 0)
    body = create_body(
        sim,
        pos=pos,
        speed=Vector.create(0, tile_size.y),
    )
    physics.update(sim, dt, body)
    # assert blocked
    assert body.speed.y == 0
    assert body.pos.y == pos.y + 1
    # assert it is sliding
    assert body.speed.x < 0
    assert body.pos.x < pos.x

    # test blocked move down, because it is a little on the left
    pos = player_cell.down().center + Vector.create(-offset.x, 0)
    body = create_body(
        sim,
        pos=pos,
        speed=Vector.create(0, tile_size.y),
    )
    physics.update(sim, dt, body)
    # assert blocked
    assert body.speed.y == 0
    assert body.pos.y == pos.y + 1
    # assert it is sliding
    assert body.speed.x > 0
    assert body.pos.x > pos.x


def test_player_no_collision():
    board = Board(
        board_size,
        tile_size
    )
    player_cell = board.by_grid(Vector.create(2, 2))
    player_cell.up().up().tile = Tiles.WALL
    player_cell.down().down().tile = Tiles.WALL
    player_cell.left().left().tile = Tiles.WALL
    player_cell.right().right().tile = Tiles.WALL

    conf = GameConfig()
    conf.friction_ratio = 1
    sim = Simulator(Context(conf, board))
    sim.on_create.append(board.on_create)
    physics = PhysicSystem(PlayerCollisionWithDTPhysic())
    shape = Shape(player_size)
    dt = 1

    # test move right
    body = create_body(
        sim,
        pos=player_cell.center,
        speed=Vector.create(tile_size.x, 0),
    )
    physics.update(sim, dt, body)
    assert body.speed == [tile_size.x, 0]
    assert body.pos == player_cell.center + Vector.create(tile_size.x, 0)
    # then block
    physics.update(sim, dt, body)
    assert body.speed == [0, 0]
    assert body.pos == player_cell.center + Vector.create(tile_size.x + 1, 0)

    # test move left
    body = create_body(
        sim,
        pos=player_cell.center,
        speed=Vector.create(-tile_size.x, 0),
    )
    physics.update(sim, dt, body)
    assert body.speed == [-tile_size.x, 0]
    assert body.pos == player_cell.center + Vector.create(-tile_size.x, 0)
    # then block
    physics.update(sim, dt, body)
    assert body.speed == [0, 0]
    assert body.pos == player_cell.center + Vector.create(-tile_size.x - 1, 0)

    # test move up
    body = create_body(
        sim,
        pos=player_cell.center,
        speed=Vector.create(0, -tile_size.y),
    )
    physics.update(sim, dt, body)
    assert body.speed == [0, -tile_size.y]
    assert body.pos == player_cell.center + Vector.create(0, -tile_size.y)
    # then block
    physics.update(sim, dt, body)
    assert body.speed == [0, 0]
    assert body.pos == player_cell.center + Vector.create(0, -tile_size.y - 1)

    # test move down
    body = create_body(
        sim,
        pos=player_cell.center,
        speed=Vector.create(0, tile_size.y),
    )
    physics.update(sim, dt, body)
    assert body.speed == [0, tile_size.y]
    assert body.pos == player_cell.center + Vector.create(0, tile_size.y)
    # then block
    physics.update(sim, dt, body)
    assert body.speed == [0, 0]
    assert body.pos == player_cell.center + Vector.create(0, tile_size.y + 1)
