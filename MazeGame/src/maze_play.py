# Walkability and one-step moves; grid letters in file are never mutated for the player.
# Player position is tracked separately in UI / text_game; S and G stay in the loaded maze data.
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
