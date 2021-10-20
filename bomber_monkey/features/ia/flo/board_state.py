from typing import Dict, Tuple, Iterator

from bomber_monkey.features.board.board import Board, BoardUpdate
from bomber_monkey.features.bomb.bomb import Bomb
from bomber_monkey.features.bomb.explosion import Explosion, ExplosionDirection
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.player.player import Player
from bomber_monkey.utils.vector import Vector

EntityId = int


class BoardState:
    def __init__(self):
        self.bombs: Dict[EntityId, Tuple[Vector, Bomb]] = {}
        self.players: Dict[EntityId, Tuple[Vector, Player]] = {}
        self.explosions: Dict[EntityId, Tuple[Vector, Explosion]] = {}

    def update(self, board: Board):
        board_updates = self._process_board_updates(board)
        return board_updates

    def _process_board_updates(self, board: Board) -> bool:
        updated = False
        for update in board.updates:
            if self._process_board_update(update, self.bombs, update.entity.get(Bomb)):
                updated = True
            if self._process_board_update(update, self.explosions, update.entity.get(Explosion)):
                updated = True
            if self._process_board_update(update, self.players, update.entity.get(Player)):
                updated = True

        return updated

    def _process_board_update(self, update: BoardUpdate, component_list, component) -> bool:
        if update.added:
            if component is None:
                return False
            component_list[update.entity.eid] = (update.position, component)
            return True
        if update.entity.eid in component_list:
            del component_list[update.entity.eid]
            return True
        return False

    def find_players(self, board: Board) -> Iterator[Vector]:
        for player_entity in board.players:
            player_pos = player_entity.get(RigidBody).pos
            player_cell = board.by_pixel(player_pos)
            yield player_entity.eid, player_cell.grid

    def find_explosion(self) -> Iterator[Tuple[Vector, int, ExplosionDirection]]:
        for bomb in self.bombs.values():
            yield bomb[0], bomb[1].explosion_size, ExplosionDirection.ALL
        for explosion in self.explosions.values():
            yield explosion[0], explosion[1].power, explosion[1].direction
