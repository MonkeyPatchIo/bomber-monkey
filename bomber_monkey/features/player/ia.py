from enum import IntEnum
from typing import Optional, Tuple, Set, List, Callable

from bomber_monkey.features.banana.banana import Banana
from bomber_monkey.features.board.board import Tiles, Cell
from bomber_monkey.features.bomb.bomb import Bomb
from bomber_monkey.features.bomb.explosion import Explosion, ExplosionDirection
from bomber_monkey.features.player.player_action import PlayerAction


class IAGaol:

    def __init__(self, action: PlayerAction, destination: Optional[Cell]):
        self.action = action
        self.destination = destination

    def __repr__(self) -> str:
        return str(self.action) + "=>" + str(self.destination)


def find_goal(body_cell: Cell) -> IAGaol:
    danger_cells: Set[Cell] = set()
    for c in find_danger_cells(body_cell):
        danger_cells.add(c)
    goal = find_action(body_cell, danger_cells)
    if goal.action != PlayerAction.NONE:
        print(goal)
    return goal


def find_danger_cells(body_cell: Cell):
    def is_bomb(c: Cell) -> bool:
        for entity in c.entities:
            if entity.get(Bomb):
                return True
        return False

    for bomb_cell in find_reachable_cells(body_cell, is_bomb):
        yield bomb_cell
        for fire_cell in find_fire_cells(bomb_cell, ExplosionDirection.LEFT):
            yield fire_cell
        for fire_cell in find_fire_cells(bomb_cell, ExplosionDirection.RIGHT):
            yield fire_cell
        for fire_cell in find_fire_cells(bomb_cell, ExplosionDirection.UP):
            yield fire_cell
        for fire_cell in find_fire_cells(bomb_cell, ExplosionDirection.DOWN):
            yield fire_cell

    def is_explosion(c: Cell) -> bool:
        for entity in c.entities:
            if entity.get(Explosion):
                return True
        return False

    for explosion_cell in find_reachable_cells(body_cell, is_explosion):
        yield explosion_cell


def find_fire_cells(bomb_cell: Cell, dir: ExplosionDirection):
    cell = bomb_cell
    while True:
        if dir == ExplosionDirection.LEFT:
            cell = cell.left()
        elif dir == ExplosionDirection.RIGHT:
            cell = cell.right()
        elif dir == ExplosionDirection.UP:
            cell = cell.up()
        elif dir == ExplosionDirection.DOWN:
            cell = cell.down()
        if cell.tile in [Tiles.WALL, Tiles.BLOCK]:
            return
        yield cell


def find_reachable_cells(body_cell: Cell, is_cell: Callable[[Cell], bool]):
    visited_cells = set()
    next_cells = [
        body_cell,
        body_cell.left(),
        body_cell.right(),
        body_cell.up(),
        body_cell.down(),
    ]
    while len(next_cells) > 0:
        cells = next_cells
        next_cells = []
        for cell in cells:
            visited_cells.add(cell)
            continue_path, is_cell_found = check_cell(cell, is_cell)
            if continue_path:
                for next_cell in walk_next(visited_cells, cell):
                    next_cells.append(next_cell)
            elif is_cell_found:
                yield cell


def check_cell(cell: Cell, is_cell: Callable[[Cell], bool]) -> Tuple[bool, bool]:
    if cell.tile in [Tiles.WALL, Tiles.BLOCK]:
        return False, False
    if is_cell(cell):
        return False, True
    return True, False


class IAGoalPath:

    @staticmethod
    def init(cell: Cell, action: PlayerAction):
        return IAGoalPath(cell, IAGaol(action, cell))

    def __init__(self, cell: Cell, goal: IAGaol):
        self.cell = cell
        self.goal = goal


def find_action(body_cell: Cell, danger_cells: Set[Cell]) -> IAGaol:
    visited_cells = set()
    visited_cells.add(body_cell)
    in_danger = body_cell in danger_cells
    next_goal_paths: List[IAGoalPath] = [
        IAGoalPath.init(body_cell.left(), PlayerAction.MOVE_LEFT),
        IAGoalPath.init(body_cell.right(), PlayerAction.MOVE_RIGHT),
        IAGoalPath.init(body_cell.up(), PlayerAction.MOVE_UP),
        IAGoalPath.init(body_cell.down(), PlayerAction.MOVE_DOWN),
    ]
    first_check = True
    while len(next_goal_paths) > 0:
        goal_paths = next_goal_paths
        next_goal_paths = []
        for goal_path in goal_paths:
            visited_cells.add(goal_path.cell)
            if not in_danger and goal_path.cell in danger_cells:
                continue
            lookup_result = check_path_lookup(goal_path.cell)
            if in_danger:
                if lookup_result in [PathLookupResult.STOP, PathLookupResult.SPECIAL_ACTION]:
                    continue
                if goal_path.cell not in danger_cells:
                    print("runnnn!")
                    return goal_path.goal
                else:
                    for next_cell in walk_next(visited_cells, goal_path.cell):
                        next_goal_paths.append(IAGoalPath(next_cell, goal_path.goal))
            else:
                if lookup_result == PathLookupResult.CONTINUE:
                    for next_cell in walk_next(visited_cells, goal_path.cell):
                        next_goal_paths.append(IAGoalPath(next_cell, goal_path.goal))
                elif lookup_result == PathLookupResult.SPECIAL_ACTION:
                    print("bomb!")
                    if first_check:
                        return pose_bomb_safely(body_cell, danger_cells)
                    else:
                        return goal_path.goal
                elif lookup_result == PathLookupResult.GO:
                    return goal_path.goal
        first_check = False
    return IAGaol(PlayerAction.NONE, None)


def pose_bomb_safely(body_cell: Cell, danger_cells: Set[Cell]) -> IAGaol:
    new_danger_cells = set(find_fire_cells(body_cell, ExplosionDirection.LEFT))\
        .union(set(find_fire_cells(body_cell, ExplosionDirection.RIGHT)))\
        .union(set(find_fire_cells(body_cell, ExplosionDirection.UP)))\
        .union(set(find_fire_cells(body_cell, ExplosionDirection.DOWN)))
    if find_safe_place(body_cell, danger_cells, new_danger_cells):
        return IAGaol(PlayerAction.MAIN_ACTION, None)
    print("Not safe!")
    return IAGaol(PlayerAction.NONE, None)


def find_safe_place(body_cell: Cell, danger_cells: Set[Cell], new_danger_cells: Set[Cell]):
    visited_cells = set()
    visited_cells.add(body_cell)
    next_cells: List[Cell] = [
        body_cell.left(),
        body_cell.right(),
        body_cell.up(),
        body_cell.down(),
    ]
    while len(next_cells) > 0:
        cells = next_cells
        next_cells = []
        for cell in cells:
            visited_cells.add(cell)
            if cell.tile in [Tiles.WALL, Tiles.BLOCK] or cell in danger_cells:
                continue
            if cell not in new_danger_cells:
                return True
            for next_cell in walk_next(visited_cells, cell):
                next_cells.append(next_cell)
    return False


class PathLookupResult(IntEnum):
    STOP = 1
    GO = 2
    SPECIAL_ACTION = 3
    CONTINUE = 4


def check_path_lookup(cell: Cell) -> PathLookupResult:
    if cell.tile == Tiles.WALL:
        return PathLookupResult.STOP
    for entity in cell.entities:
        if entity.get(Bomb) or entity.get(Explosion):
            return PathLookupResult.STOP
        if entity.get(Banana):
            return PathLookupResult.GO
    if cell.tile == Tiles.BLOCK:
        return PathLookupResult.SPECIAL_ACTION
    return PathLookupResult.CONTINUE


def walk_next(visited_cells: Set[Cell], cell: Cell):
    next_cell = cell.left()
    if next_cell not in visited_cells:
        yield next_cell
    next_cell = cell.right()
    if next_cell not in visited_cells:
        yield next_cell
    next_cell = cell.up()
    if next_cell not in visited_cells:
        yield next_cell
    next_cell = cell.down()
    if next_cell not in visited_cells:
        yield next_cell
