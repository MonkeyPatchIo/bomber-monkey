from bomber_monkey.features.board.board import Tiles
from bomber_monkey.features.lifetime.lifetime import Lifetime
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.spawner.spawner import Spawner
from bomber_monkey.game_config import GameConfig
from bomber_monkey.game_factory import GameFactory
from bomber_monkey.states.game_state import GameState
from bomber_monkey.states.state_manager import StateManager
from bomber_monkey.utils.vector import Vector


class DummyAvatar:
    def __init__(self, pos):
        self.body = RigidBody(pos=pos)
        self.dropper = Spawner(drop_rate=0, factory=lambda: None)

    def get(self, component):
        if component == RigidBody:
            return self.body
        if component == Spawner:
            return self.dropper
        raise 'DummyAvatar: Unsupported component type "{}"'.format(component)


class Init:
    def __init__(self, blocks=None, bombs=None):
        self.bombs = bombs or [(2, 2, True)]
        self.blocks = blocks or []


def assert_system_update(init: Init, expected_tiles):
    conf: GameConfig = GameConfig()
    conf.bomb_duration = 999999999  # Pseudo-infinite
    conf.bomb_power = 2
    conf.resources_path = '../bomber_monkey/resources/'
    state: GameState = GameState(state_manager=StateManager(), conf=conf)
    state.init()

    for (x, y) in init.blocks:
        state.board.by_grid(Vector.create(x, y)).tile = Tiles.BLOCK

    for (x, y, expire) in init.bombs:
        cell = state.board.by_grid(Vector.create(x, y))
        bomb = GameFactory.create_bomb(state.sim, RigidBody(pos=cell.center))
        if expire:
            life: Lifetime = bomb.get(Lifetime)
            life.expire()

        state.sim.update()

    for (x, y, expected) in expected_tiles:
        actual = state.board.by_grid(Vector.create(x, y)).tile
        assert actual == expected, '{},{} -> {}   ==   {}'.format(x, y, actual, expected)


def test_empty_grid():
    init = Init()

    expecteds = [
        (0, 2, Tiles.EMPTY),
        (1, 2, Tiles.EMPTY),
        (2, 2, Tiles.EMPTY),
        (3, 2, Tiles.EMPTY),
        (4, 2, Tiles.EMPTY),

        (2, 0, Tiles.EMPTY),
        (2, 1, Tiles.EMPTY),
        (2, 2, Tiles.EMPTY),
        (2, 3, Tiles.EMPTY),
        (2, 4, Tiles.EMPTY)
    ]

    assert_system_update(init, expecteds)


def test_top_block():
    init = Init(blocks=[
        (2, 0),
        (2, 1)
    ])

    expecteds = [
        (0, 2, Tiles.EMPTY),
        (1, 2, Tiles.EMPTY),
        (2, 2, Tiles.EMPTY),
        (3, 2, Tiles.EMPTY),
        (4, 2, Tiles.EMPTY),

        (2, 0, Tiles.BLOCK),
        (2, 1, Tiles.EMPTY),
        (2, 2, Tiles.EMPTY),
        (2, 3, Tiles.EMPTY),
        (2, 4, Tiles.EMPTY)
    ]

    assert_system_update(init, expecteds)


def test_top_two_block():
    init = Init(blocks=[
        (2, 0)
    ])

    expecteds = [
        (0, 2, Tiles.EMPTY),
        (1, 2, Tiles.EMPTY),
        (2, 2, Tiles.EMPTY),
        (3, 2, Tiles.EMPTY),
        (4, 2, Tiles.EMPTY),

        (2, 0, Tiles.EMPTY),
        (2, 1, Tiles.EMPTY),
        (2, 2, Tiles.EMPTY),
        (2, 3, Tiles.EMPTY),
        (2, 4, Tiles.EMPTY)
    ]

    assert_system_update(init, expecteds)


def test_right_block():
    init = Init(blocks=[
        (3, 2),
        (4, 2)
    ])

    expecteds = [
        (0, 2, Tiles.EMPTY),
        (1, 2, Tiles.EMPTY),
        (2, 2, Tiles.EMPTY),
        (3, 2, Tiles.EMPTY),
        (4, 2, Tiles.BLOCK),

        (2, 0, Tiles.EMPTY),
        (2, 1, Tiles.EMPTY),
        (2, 2, Tiles.EMPTY),
        (2, 3, Tiles.EMPTY),
        (2, 4, Tiles.EMPTY)
    ]

    assert_system_update(init, expecteds)


def test_bottom_block():
    init = Init(blocks=[
        (2, 3),
        (2, 4)
    ])

    expecteds = [
        (0, 2, Tiles.EMPTY),
        (1, 2, Tiles.EMPTY),
        (2, 2, Tiles.EMPTY),
        (3, 2, Tiles.EMPTY),
        (4, 2, Tiles.EMPTY),

        (2, 0, Tiles.EMPTY),
        (2, 1, Tiles.EMPTY),
        (2, 2, Tiles.EMPTY),
        (2, 3, Tiles.EMPTY),
        (2, 4, Tiles.BLOCK)
    ]

    assert_system_update(init, expecteds)


def test_left_block():
    init = Init(blocks=[
        (0, 2),
        (1, 2)
    ])

    expecteds = [
        (0, 2, Tiles.BLOCK),
        (1, 2, Tiles.EMPTY),
        (2, 2, Tiles.EMPTY),
        (3, 2, Tiles.EMPTY),
        (4, 2, Tiles.EMPTY),

        (2, 0, Tiles.EMPTY),
        (2, 1, Tiles.EMPTY),
        (2, 2, Tiles.EMPTY),
        (2, 3, Tiles.EMPTY),
        (2, 4, Tiles.EMPTY)
    ]

    assert_system_update(init, expecteds)


def test_bomb_chain_two():
    init = Init(
        blocks=[
            (0, 0), (1, 0), (2, 0), (3, 0), (4, 0),
            (0, 1), (1, 1), (2, 1), (3, 1), (4, 1),
            (0, 2), (1, 2), (3, 2), (4, 2),
            (0, 3), (1, 3), (3, 3), (4, 3),
            (0, 4), (1, 4), (2, 4), (3, 4), (4, 4),
            (0, 5), (1, 5), (2, 5), (3, 5), (4, 5),
        ],
        bombs=[
            (2, 2, True),
            (2, 3, False),
        ]
    )

    expecteds = [
        (0, 0, Tiles.BLOCK), (1, 0, Tiles.BLOCK), (2, 0, Tiles.BLOCK), (3, 0, Tiles.BLOCK), (4, 0, Tiles.BLOCK),
        (0, 1, Tiles.BLOCK), (1, 1, Tiles.BLOCK), (2, 1, Tiles.EMPTY), (3, 1, Tiles.BLOCK), (4, 1, Tiles.BLOCK),
        (0, 2, Tiles.BLOCK), (1, 2, Tiles.EMPTY), (2, 2, Tiles.EMPTY), (3, 2, Tiles.EMPTY), (4, 2, Tiles.BLOCK),
        (0, 3, Tiles.BLOCK), (1, 3, Tiles.EMPTY), (2, 3, Tiles.EMPTY), (3, 3, Tiles.EMPTY), (4, 3, Tiles.BLOCK),
        (0, 4, Tiles.BLOCK), (1, 4, Tiles.BLOCK), (2, 4, Tiles.EMPTY), (3, 4, Tiles.BLOCK), (4, 4, Tiles.BLOCK),
        (0, 5, Tiles.BLOCK), (1, 5, Tiles.BLOCK), (2, 5, Tiles.BLOCK), (3, 5, Tiles.BLOCK), (4, 5, Tiles.BLOCK),
    ]

    assert_system_update(init, expecteds)
