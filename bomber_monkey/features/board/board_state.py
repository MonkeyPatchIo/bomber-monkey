from typing import Dict, Tuple, Iterator

from bomber_monkey.features.board.board_update import BoardUpdate
from bomber_monkey.features.bomb.bomb import Bomb
from bomber_monkey.features.bomb.explosion import Explosion, ExplosionDirection
from bomber_monkey.features.items.banana import Banana
from bomber_monkey.features.items.immunity import ImmunityItem
from bomber_monkey.features.player.player import Player
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import Simulator

EntityId = int


class BoardState:
    def __init__(self):
        self.bombs: Dict[EntityId, Tuple[Vector, Bomb]] = {}
        self.bananas: Dict[EntityId, Tuple[Vector, Banana]] = {}
        self.immunities: Dict[EntityId, Tuple[Vector, ImmunityItem]] = {}
        self.players: Dict[EntityId, Tuple[Vector, Player]] = {}
        self.explosions: Dict[EntityId, Tuple[Vector, Explosion]] = {}
        self.last_update = -1
        self.is_updated = False

        self.to_process = {
            Bomb: self.bombs,
            ImmunityItem: self.immunities,
            Banana: self.bananas,
            Explosion: self.explosions,
            Player: self.players
        }

    def update(self, sim: Simulator):
        from bomber_monkey.features.board.board import Board
        self.last_update = sim.last_update
        board: Board = sim.context.board

        status = False
        for update in board.updates:
            status = self.handle_update(update)
        self.is_updated = status

    def handle_update(self, update: BoardUpdate):
        status = False
        for component_type, collection in self.to_process.items():
            component = update.entity.get(component_type)
            if _process_board_update(update, collection, component):
                status = True
        return status

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
