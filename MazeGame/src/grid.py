# Shared maze representation: list of rows, each row a list of single-character cells.
# Row 0 is the top line of the file; col 0 is the leftmost character (matches on-screen layout).
from __future__ import annotations

from typing import List

# Characters used in level .txt files (must match examples/*.txt).
WALL = "#"
FLOOR = "."
START = "S"
GOAL = "G"


def grid_dimensions(grid: List[List[str]]) -> tuple[int, int]:
    # (row_count, col_count); empty grid yields (0, 0).
    return len(grid), len(grid[0]) if grid else 0


def in_bounds(grid: List[List[str]], row: int, col: int) -> bool:
    # False if row/col negative or past the last row/column.
    rows, cols = grid_dimensions(grid)
    return 0 <= row < rows and 0 <= col < cols


def copy_grid(grid: List[List[str]]) -> List[List[str]]:
    # Shallow copy per row so mutating the copy does not change the original maze.
    return [list(row) for row in grid]


def overlay_path(
    base_grid: List[List[str]],
    path: List[tuple[int, int]],
    player_pos: tuple[int, int],
    path_char: str = "o",
) -> List[List[str]]:
    # Build a printable grid: path cells marked, player always shown as P on top.
    # The file-backed grid is unchanged elsewhere; this is only for text-mode display.
    display = copy_grid(base_grid)
    pr, pc = player_pos
    for r, c in path:
        # Player cell gets P at the end, not 'o'.
        if (r, c) == (pr, pc):
            continue
        ch = display[r][c]
        # Do not paint over start/goal markers — keep S and G readable.
        if ch not in (START, GOAL):
            display[r][c] = path_char
    display[pr][pc] = "P"
    return display
