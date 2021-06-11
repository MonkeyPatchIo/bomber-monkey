from enum import IntEnum
from typing import Optional, Tuple, Set, List, Iterator, Dict

from bomber_monkey.features.banana.banana import Banana
from bomber_monkey.features.board.board import Tiles, Cell, Board, BoardUpdate
from bomber_monkey.features.bomb.bomb import Bomb
from bomber_monkey.features.bomb.explosion import Explosion, ExplosionDirection
from bomber_monkey.features.ia.ia_controller_system import IA
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.player.player import Player
from bomber_monkey.features.player.player_action import PlayerAction
from bomber_monkey.utils.vector import Vector
from python_ecs.ecs import Simulator


DEBUG_IA = False

class IAGaol:

    def __init__(self, action: PlayerAction, description: str = "meh"):
        self.action = action
        self.description = description

    def __repr__(self) -> str:
        return f"{self.action}: {self.description}"


class NicoIA(IA):
    def __init__(self):
        self.current_goal = None
        self.bombs: Dict[int, Tuple[Vector, Bomb]] = {}
        self.explosions: Dict[int, Tuple[Vector, Explosion]] = {}
        self.danger_positions: Set[Vector] = set()
        self.attack_positions: Set[Vector] = set()
        self.other_player_positions: Dict[int, Vector] = {}

    def get_action(self, sim: Simulator, body: RigidBody) -> PlayerAction:
        board: Board = sim.context.board
        player: Player = body.entity().get(Player)
        if self.current_goal is not None and len(board.updates) == 0:
            return self.current_goal.action

        if len(board.updates) > 0 and self.process_board_updates(board):
            self.danger_positions = set(self.find_danger_positions(board))
            if DEBUG_IA:
                print(f"danger_positions={self.danger_positions}")

        if self.update_player_positions(board, player):
            self.attack_positions = set(self.find_attack_positions(board, player))
            if DEBUG_IA:
                print(f"attack_positions={self.attack_positions}")

        body_cell = board.by_pixel(body.pos)
        goal = self.find_action(board, body_cell, player)
        if DEBUG_IA:
            print(goal)
        self.current_goal = goal
        return goal.action

    def process_board_updates(self, board: Board) -> bool:
        updated = False
        for update in board.updates:
            if DEBUG_IA:
                print(f"processing update: {update}")
            if self.process_board_update(update, self.bombs, update.entity.get(Bomb)):
                updated = True
            if self.process_board_update(update, self.explosions, update.entity.get(Explosion)):
                updated = True
        if DEBUG_IA:
            print(f"bombs={self.bombs}")
            print(f"explosions={self.explosions}")
        return updated

    def process_board_update(self, update: BoardUpdate, component_list, component) -> bool:
        if update.added:
            if component is None:
                return False
            component_list[update.entity.eid] = (update.position, component)
            return True
        if update.entity.eid in component_list:
            del component_list[update.entity.eid]
            return True
        return False

    def find_danger_positions(self, board: Board) -> Iterator[Vector]:
        for position, size, direction in self.find_explosion():
            yield position
            if direction & ExplosionDirection.LEFT:
                yield from find_fire_cells(board, position, ExplosionDirection.LEFT, size)
            if direction & ExplosionDirection.RIGHT:
                yield from find_fire_cells(board, position, ExplosionDirection.RIGHT, size)
            if direction & ExplosionDirection.UP:
                yield from find_fire_cells(board, position, ExplosionDirection.UP, size)
            if direction & ExplosionDirection.DOWN:
                yield from find_fire_cells(board, position, ExplosionDirection.DOWN, size)

    def find_explosion(self) -> Iterator[Tuple[Vector, int, ExplosionDirection]]:
        for bomb in self.bombs.values():
            yield bomb[0], bomb[1].explosion_size, ExplosionDirection.ALL
        for explosion in self.explosions.values():
            yield explosion[0], explosion[1].power, explosion[1].direction

    def update_player_positions(self, board: Board, self_player: Player):
        updated = False
        for eid, position in self.find_other_players(board, self_player):
            if eid not in self.other_player_positions or self.other_player_positions[eid] != position:
                self.other_player_positions[eid] = position
                updated = True
        return updated

    def find_other_players(self, board: Board, self_player: Player) -> Iterator[Vector]:
        for player_entity in board.players:
            if self_player.player_id == player_entity.get(Player).player_id:
                continue
            player_pos = player_entity.get(RigidBody).pos
            player_cell = board.by_pixel(player_pos)
            yield player_entity.eid, player_cell.grid

    def find_attack_positions(self, board: Board, self_player: Player) -> Iterator[Vector]:
        for player_entity in board.players:
            if self_player.player_id == player_entity.get(Player).player_id:
                continue
            player_pos = player_entity.get(RigidBody).pos
            player_cell = board.by_pixel(player_pos)
            yield player_cell.grid
            yield from find_fire_cells(board, player_cell.grid, ExplosionDirection.LEFT, self_player.power)
            yield from find_fire_cells(board, player_cell.grid, ExplosionDirection.RIGHT, self_player.power)
            yield from find_fire_cells(board, player_cell.grid, ExplosionDirection.UP, self_player.power)
            yield from find_fire_cells(board, player_cell.grid, ExplosionDirection.DOWN, self_player.power)

    def find_action(self, board: Board, body_cell: Cell, player: Player) -> IAGaol:
        visited_positions = set()
        visited_positions.add(body_cell.grid)
        in_danger = body_cell.grid in self.danger_positions
        next_goal_paths: List[IAGoalPath] = [
            IAGoalPath(body_cell, body_cell.left(), ExplosionDirection.LEFT, PlayerAction.MOVE_LEFT),
            IAGoalPath(body_cell, body_cell.right(), ExplosionDirection.RIGHT, PlayerAction.MOVE_RIGHT),
            IAGoalPath(body_cell, body_cell.up(), ExplosionDirection.UP, PlayerAction.MOVE_UP),
            IAGoalPath(body_cell, body_cell.down(), ExplosionDirection.DOWN, PlayerAction.MOVE_DOWN),
        ]
        first_check = True
        while len(next_goal_paths) > 0:
            goal_paths = next_goal_paths
            next_goal_paths = []
            for goal_path in goal_paths:
                visited_positions.add(goal_path.next_cell.grid)
                if not in_danger and goal_path.next_cell.grid in self.danger_positions:
                    continue
                if not in_danger and goal_path.next_cell.grid in self.attack_positions and self.can_place_bomb_safely(board, goal_path.next_cell, player):
                    if first_check:
                        return IAGaol(PlayerAction.MAIN_ACTION, "Attack!")
                    else:
                        return IAGaol(goal_path.action, f"Go to attack on {goal_path.next_cell.grid}!")
                target_action = check_cell_content(goal_path.next_cell, player)
                if in_danger:
                    if target_action in [TargetAction.STOP, TargetAction.BOMB]:
                        continue
                    if goal_path.next_cell.grid not in self.danger_positions:
                        return IAGaol(goal_path.action, f"escaping to {goal_path.next_cell.grid}")
                    else:
                        for next_cell, direction in walk_next(visited_positions, goal_path.next_cell, goal_path.direction):
                            next_goal_paths.append(IAGoalPath(goal_path.next_cell, next_cell, direction, goal_path.action))
                else:
                    if target_action == TargetAction.CONTINUE:
                        for next_cell, direction in walk_next(visited_positions, goal_path.next_cell, goal_path.direction):
                            next_goal_paths.append(IAGoalPath(goal_path.next_cell, next_cell, direction, goal_path.action))
                    elif target_action == TargetAction.BOMB and self.can_place_bomb_safely(board, goal_path.from_cell, player):
                        if first_check:
                            return IAGaol(PlayerAction.MAIN_ACTION, "Bomb!")
                        else:
                            return IAGaol(goal_path.action, f"Go to bomb on {goal_path.next_cell.grid}!")
                    elif target_action == TargetAction.GO:
                        return IAGaol(goal_path.action, f"going to {goal_path.next_cell.grid}")
            first_check = False
        if in_danger:
            return IAGaol(PlayerAction.NONE, "I am fucked up")
        return IAGaol(PlayerAction.NONE, "boring!")

    def can_place_bomb_safely(self, board: Board, cell: Cell, player: Player) -> bool:
        bomb_size = player.power
        new_danger_positions = {cell.grid} \
            .union(set(find_fire_cells(board, cell.grid, ExplosionDirection.LEFT, bomb_size))) \
            .union(set(find_fire_cells(board, cell.grid, ExplosionDirection.RIGHT, bomb_size))) \
            .union(set(find_fire_cells(board, cell.grid, ExplosionDirection.UP, bomb_size))) \
            .union(set(find_fire_cells(board, cell.grid, ExplosionDirection.DOWN, bomb_size)))
        if DEBUG_IA:
            print(f"from {cell.grid} new_danger_positions={new_danger_positions}")
        return self.find_safe_place(cell, new_danger_positions)

    def find_safe_place(self, body_cell: Cell, new_danger_positions: Set[Vector]):
        visited_positions = set()
        visited_positions.add(body_cell.grid)
        next_cells: List[Tuple[Cell, ExplosionDirection]] = [
            (body_cell.left(), ExplosionDirection.LEFT),
            (body_cell.right(), ExplosionDirection.RIGHT),
            (body_cell.up(), ExplosionDirection.UP),
            (body_cell.down(), ExplosionDirection.DOWN),
        ]
        while len(next_cells) > 0:
            cells = next_cells
            next_cells = []
            for cell, direction in cells:
                visited_positions.add(cell.grid)
                if cell.tile in [Tiles.WALL, Tiles.BLOCK] or cell.grid in self.danger_positions:
                    continue
                if cell.grid not in new_danger_positions:
                    if DEBUG_IA:
                        print(f"{cell.grid} is safe")
                    return True
                for next_cell in walk_next(visited_positions, cell, direction):
                    next_cells.append(next_cell)
        return False


def find_fire_cells(board: Board, grid: Vector, direction: ExplosionDirection, bomb_size: int) -> Iterator[Vector]:
    cell = board.by_grid(grid)
    while bomb_size > 0:
        if direction == ExplosionDirection.LEFT:
            cell = cell.left()
        elif direction == ExplosionDirection.RIGHT:
            cell = cell.right()
        elif direction == ExplosionDirection.UP:
            cell = cell.up()
        elif direction == ExplosionDirection.DOWN:
            cell = cell.down()
        if cell.tile in [Tiles.WALL, Tiles.BLOCK]:
            return
        bomb_size = bomb_size - 1
        yield cell.grid


class IAGoalPath:

    def __init__(self, from_cell: Cell, next_cell: Cell, direction: ExplosionDirection, action: PlayerAction):
        self.from_cell = from_cell
        self.next_cell = next_cell
        self.direction = direction
        self.action = action


class TargetAction(IntEnum):
    STOP = 1
    GO = 2
    BOMB = 3
    CONTINUE = 4


def check_cell_content(cell: Cell, player: Player) -> TargetAction:
    if cell.tile == Tiles.WALL:
        return TargetAction.STOP
    for entity in cell.entities:
        if entity.get(Banana):
            return TargetAction.GO
    if cell.tile == Tiles.BLOCK:
        return TargetAction.BOMB
    return TargetAction.CONTINUE


def walk_next(visited_positions: Set[Vector], cell: Cell, direction: ExplosionDirection):
    if direction != ExplosionDirection.RIGHT:
        next_cell = cell.left()
        if next_cell.grid not in visited_positions:
            yield next_cell, ExplosionDirection.LEFT
    if direction != ExplosionDirection.LEFT:
        next_cell = cell.right()
        if next_cell.grid not in visited_positions:
            yield next_cell, ExplosionDirection.RIGHT
    if direction != ExplosionDirection.DOWN:
        next_cell = cell.up()
        if next_cell.grid not in visited_positions:
            yield next_cell, ExplosionDirection.UP
    if direction != ExplosionDirection.UP:
        next_cell = cell.down()
        if next_cell.grid not in visited_positions:
            yield next_cell, ExplosionDirection.DOWN
