# Public API: re-exports so code can `from game_logic import ...` without knowing split modules.
# Split keeps `directions` / `maze_load` / `maze_play` small; this file is the stable import surface.
from __future__ import annotations

from directions import DIRECTION_DELTAS, DOWN, LEFT, RIGHT, UP
from maze_load import find_start_goal, load_grid
from maze_play import check_win, is_walkable, move_player
