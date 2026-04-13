# Draw maze tiles and player on a Tk Canvas (called after canvas.delete("all")).
# Order: maze layer first, then player — so the blue square is never hidden under a floor tile.
from __future__ import annotations

import tkinter as tk
from typing import List, Set, Tuple

from grid import GOAL, START, WALL

from .constants import (
    COLOR_FLOOR,
    COLOR_GOAL,
    COLOR_PATH,
    COLOR_START,
    COLOR_WALL,
    CELL_PX,
    UI_BORDER,
)
from .player import cell_rect, draw_player


def _base_color_for_cell(character: str) -> str:
    """Colour for the maze letter in the file (before path highlighting)."""
    if character == WALL:
        return COLOR_WALL
    if character == START:
        return COLOR_START
    if character == GOAL:
        return COLOR_GOAL
    return COLOR_FLOOR


def draw_maze_layer(
    canvas: tk.Canvas,
    maze: List[List[str]],
    path_set: Set[Tuple[int, int]],
) -> None:
    """Draw every cell as a rectangle. Cells on the path turn yellow (except S and G)."""
    rows = len(maze)
    cols = len(maze[0]) if rows else 0

    for row in range(rows):
        for col in range(cols):
            character = maze[row][col]
            fill_color = _base_color_for_cell(character)

            on_path = (row, col) in path_set
            keep_start_or_goal_color = character in (START, GOAL)
            if on_path and not keep_start_or_goal_color:
                fill_color = COLOR_PATH

            x0, y0, x1, y1 = cell_rect(row, col, CELL_PX)
            canvas.create_rectangle(x0, y0, x1, y1, outline=UI_BORDER, fill=fill_color)


def draw_player_on_maze(
    canvas: tk.Canvas,
    player_pos: Tuple[int, int],
) -> None:
    """Call after the maze layer so the player is drawn on top."""
    player_row, player_col = player_pos
    draw_player(canvas, player_row, player_col, CELL_PX)
