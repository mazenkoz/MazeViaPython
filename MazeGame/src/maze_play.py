# Core movement rules: which cells are walkable and how one keypress updates the player.
# The grid loaded from disk is not edited when the player walks — start/goal letters remain
# ``S`` and ``G``; UIs keep ``(row, col)`` for the avatar and pass it into move_player().
#
# is_walkable() treats anything except ``#`` as passable inside bounds. move_player() maps a
# direction string (see ``directions``) to a delta and returns the old position if blocked.
# check_win() compares player tuple to goal tuple (standing on ``G``).
from __future__ import annotations

from typing import List, Tuple

from directions import DIRECTION_DELTAS
from grid import WALL, in_bounds


def is_walkable(grid: List[List[str]], row: int, col: int) -> bool:
    # Inside the grid and not a wall (#). S and G count as walkable.
    return in_bounds(grid, row, col) and grid[row][col] != WALL


def move_player(
    grid: List[List[str]], player_pos: Tuple[int, int], direction: str
) -> Tuple[int, int]:
    # One step in direction; returns old position if the target cell is blocked or out of bounds.
    if direction not in DIRECTION_DELTAS:
        raise ValueError(f"Unknown direction: {direction!r}")
    dr, dc = DIRECTION_DELTAS[direction]
    r, c = player_pos
    nr, nc = r + dr, c + dc
    return (nr, nc) if is_walkable(grid, nr, nc) else player_pos


def check_win(player_pos: Tuple[int, int], goal_pos: Tuple[int, int]) -> bool:
    # Win when player coordinates equal goal coordinates (standing on G).
    return player_pos == goal_pos
