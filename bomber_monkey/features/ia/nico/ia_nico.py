import logging
from typing import Tuple, Set, List

from bomber_monkey.features.board.board import Tiles, Cell, Board
from bomber_monkey.features.bomb.explosion import ExplosionDirection
from bomber_monkey.features.ia.ia_interface import IA
from bomber_monkey.features.ia.nico.utils import find_danger_positions, find_attack_positions, IAGaol, IAGoalPath, \
    check_cell_content, TargetAction, walk_next, find_fire_cells
from bomber_monkey.features.physics.rigid_body import RigidBody
from bomber_monkey.features.player.player import Player
from bomber_monkey.features.player.player_action import PlayerAction
from bomber_monkey.utils.vector import Vector

logger = logging.getLogger(__name__)


class NicoIA(IA):
    def __init__(self):
        super().__init__()
        self.current_goal = None
        self.danger_positions: Set[Vector] = set()
        self.attack_positions: Set[Vector] = set()

    def get_action(self, board: Board, body: RigidBody) -> PlayerAction:
        player: Player = body.entity().get(Player)
        player_pos: Vector = body.pos
        body_cell = board.by_pixel(player_pos)

        state = board.state
        board_updated = state.is_updated

        if board_updated:
            self.current_goal = None

        if self.current_goal:
            return self.current_goal.action

        self.danger_positions = set(find_danger_positions(board))
        self.attack_positions = set(find_attack_positions(board, player))
        logger.debug(f"danger_positions={self.danger_positions}")
        logger.debug(f"attack_positions={self.attack_positions}")

        goal = self.find_action(board, body_cell, player)
        logger.debug(goal)
        self.current_goal = goal
        return goal.action

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
                if not in_danger and goal_path.next_cell.grid in self.attack_positions and self.can_place_bomb_safely(
                        board, goal_path.next_cell, player):
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
                        for next_cell, direction in walk_next(visited_positions, goal_path.next_cell,
                                                              goal_path.direction):
                            next_goal_paths.append(
                                IAGoalPath(goal_path.next_cell, next_cell, direction, goal_path.action))
                else:
                    if target_action == TargetAction.CONTINUE:
                        for next_cell, direction in walk_next(visited_positions, goal_path.next_cell,
                                                              goal_path.direction):
                            next_goal_paths.append(
                                IAGoalPath(goal_path.next_cell, next_cell, direction, goal_path.action))
                    elif target_action == TargetAction.BOMB and self.can_place_bomb_safely(board, goal_path.from_cell,
                                                                                           player):
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
        logger.debug(f"from {cell.grid} new_danger_positions={new_danger_positions}")
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
                    logger.debug(f"{cell.grid} is safe")
                    return True
                for next_cell in walk_next(visited_positions, cell, direction):
                    next_cells.append(next_cell)
        return False
