from bomber_monkey.features.banana.banana import Banana
from bomber_monkey.features.destruction.destruction import Destruction, Protection
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.player.player import Player
from bomber_monkey.utils.collision_detector import detect_collision
from python_ecs.ecs import System, Simulator


class DestructionSystem(System):

    def __init__(self):
        super().__init__([Destruction, RigidBody])

    def update(self, sim: Simulator, dt: float, destruction: Destruction, body: RigidBody) -> None:
        cell = sim.context.board.by_pixel(body.pos)
        entities = cell.get(Banana, Player)
        for entity in entities:
            if entity:
                entity_body: RigidBody = entity.get(RigidBody)
                protection: Protection = entity.get(Protection)
                if detect_collision(body, entity_body):
                    if not protection or protection.remaining <= 0:
                        entity.destroy()
