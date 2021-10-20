from typing import Optional

from python_ecs.ecs import Component
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.player.player import Player
from bomber_monkey.utils.collision_detector import detect_collision
from python_ecs.ecs import Simulator


def consume_item(sim: Simulator, item: Component, body: RigidBody) -> Optional[Player]:
    cell = sim.context.board.by_pixel(body.pos)
    for _ in filter(None, [cell, cell.right(), cell.left(), cell.down(), cell.up()]):
        for player_entity in _.get(Player):
            item_body: RigidBody = player_entity.get(RigidBody)
            if detect_collision(body, item_body):
                item.entity().destroy()
                return player_entity.get(Player)
    return None
