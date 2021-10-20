from enum import IntEnum

from bomber_monkey.features.physics.rigid_body import RigidBody

from bomber_monkey.features.spawner.spawner import Spawner
from bomber_monkey.game_config import GameConfig
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import Simulator


class PlayerAction(IntEnum):
    NONE = 0
    MOVE_LEFT = 1
    MOVE_RIGHT = 2
    MOVE_UP = 4
    MOVE_DOWN = 8
    MAIN_ACTION = 16
    CANCEL = 32


def apply_action(sim: Simulator, action: PlayerAction, body: RigidBody):
    conf: GameConfig = sim.context.conf
    if action is None:
        return

    if action & PlayerAction.MOVE_LEFT:
        body.accel = Vector.create(-conf.player_accel, body.accel.y)

    if action & PlayerAction.MOVE_RIGHT:
        body.accel = Vector.create(conf.player_accel, body.accel.y)

    if action & PlayerAction.MOVE_UP:
        body.accel = Vector.create(body.accel.x, -conf.player_accel)

    if action & PlayerAction.MOVE_DOWN:
        body.accel = Vector.create(body.accel.x, conf.player_accel)

    if action & PlayerAction.MAIN_ACTION:
        dropper: Spawner = body.entity().get(Spawner)
        dropper.produce(body)

    if action & PlayerAction.CANCEL:
        sim.context.pause_game()
