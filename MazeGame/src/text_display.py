# Helpers for the terminal maze view: pretty-printing and building a display copy of the grid.
# format_grid_lines joins rows for printing; build_display overlays the player (and optional
# shortest-path cells) using grid.copy_grid / grid.overlay_path so the canonical maze from
# maze_load is never mutated when the user moves.
#
# default_level_path points at the bundled examples/level1.txt under the project root.
# print_help emits the one-screen control summary when a text session starts.
from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Tuple

from grid import copy_grid, overlay_path


def default_level_path() -> str:
    # Shipped maze used when no path is passed on the command line.
    return str(Path(__file__).resolve().parent.parent / "examples" / "level1.txt")


def format_grid_lines(grid: List[List[str]]) -> str:
    # One string per row, joined with newlines for printing.
    return "\n".join("".join(row) for row in grid)


def build_display(
    base_grid: List[List[str]],
    player_pos: Tuple[int, int],
    path_cells: Optional[List[Tuple[int, int]]],
) -> List[List[str]]:
    # If path is active, use overlay_path; else copy grid and place P on the player cell.
    if path_cells:
        return overlay_path(base_grid, path_cells, player_pos)
    display = copy_grid(base_grid)
    r, c = player_pos
    display[r][c] = "P"
    return display


def print_help() -> None:
    # One-shot hint printed at game start.
    print("\nCommands: w/a/s/d = move | p = shortest path | q = quit\n")
