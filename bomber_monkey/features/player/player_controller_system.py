from bomber_monkey.features.lifetime.lifetime import Lifetime
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.player.player_controller import PlayerController, PlayerAction
from bomber_monkey.features.spawner.spawner import Spawner
from bomber_monkey.game_config import GameConfig
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import System, Simulator


class PlayerControllerSystem(System):

    def __init__(self):
        super().__init__([RigidBody, PlayerController])

    def update(self, sim: Simulator, dt: float, body: RigidBody, player_controller: PlayerController):
        if sim.context.game_elapsed_time < sim.context.conf.game_startup_delay:
            return
        lifetime: Lifetime = body.entity().get(Lifetime)
        if lifetime is not None and lifetime.is_expiring():
            return

        conf: GameConfig = sim.context.conf

        action = player_controller.get_action()

        if action & PlayerAction.MOVE_LEFT:
            body.accel = Vector.create(-conf.player_accel, body.accel.y)

        if action & PlayerAction.MOVE_RIGHT:
            body.accel = Vector.create(conf.player_accel, body.accel.y)

        if action & PlayerAction.MOVE_UP:
            body.accel = Vector.create(body.accel.x, -conf.player_accel)

        if action & PlayerAction.MOVE_DOWN:
            body.accel = Vector.create(body.accel.x, conf.player_accel)

        if action & PlayerAction.SPECIAL_ACTION:
            dropper: Spawner = body.entity().get(Spawner)
            dropper.produce(body)
