# Helpers for the terminal (text) maze view: formatting and merging player/path onto the grid.
# The text game prints these strings; the underlying maze list from load_grid is not edited for movement.
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
