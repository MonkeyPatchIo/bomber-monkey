from typing import Dict, Tuple, Iterator

from bomber_monkey.features.board.board_update import BoardUpdate
from bomber_monkey.features.bomb.bomb import Bomb
from bomber_monkey.features.bomb.explosion import Explosion, ExplosionDirection
from bomber_monkey.features.items.banana import Banana
from bomber_monkey.features.player.player import Player
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import Simulator

EntityId = int


class BoardState:
    def __init__(self):
        self.bombs: Dict[EntityId, Tuple[Vector, Bomb]] = {}
        self.bananas: Dict[EntityId, Tuple[Vector, Banana]] = {}
        self.players: Dict[EntityId, Tuple[Vector, Player]] = {}
        self.explosions: Dict[EntityId, Tuple[Vector, Explosion]] = {}
        self.last_update = -1
        self.is_updated = False

        self.to_process = {
            Bomb: self.bombs,
            Banana: self.bananas,
            Explosion: self.explosions,
            Player: self.players
        }

    def update(self, sim: Simulator):
        from bomber_monkey.features.board.board import Board

        if self.last_update >= sim.last_update:
            return
        self.last_update = sim.last_update

        board: Board = sim.context.board

        self.is_updated = False
        for update in board.updates:
            for item_type, collection in self.to_process.items():
                if _process_board_update(update, collection, update.entity.get(item_type)):
                    self.is_updated = True

    def explosions_iter(self) -> Iterator[Tuple[Vector, int, ExplosionDirection]]:
        for bomb in self.bombs.values():
            yield bomb[0], bomb[1].explosion_size, ExplosionDirection.ALL
        for explosion in self.explosions.values():
            yield explosion[0], explosion[1].power, explosion[1].direction


def _process_board_update(update: BoardUpdate, component_list, component) -> bool:
    if update.added:
        if component is None:
            return False
        component_list[update.entity.eid] = (update.position, component)
        return True
    if update.entity.eid in component_list:
        del component_list[update.entity.eid]
        return True
    return False
