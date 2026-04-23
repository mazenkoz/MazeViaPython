# Direction vocabulary and grid deltas shared by the GUI key map and maze_play.move_player().
# UP/DOWN/LEFT/RIGHT are plain strings so logs and tests stay readable and distinct from Tk
# keysyms like ``Up`` / ``Return``.
#
# DIRECTION_DELTAS maps each direction to (d_row, d_col) with row growing downward — must stay
# aligned with gui.constants.KEY_TO_DIR so arrow keys and WASD feed the same move_player API.
from __future__ import annotations

# Strings passed into move_player; must match gui.constants.KEY_TO_DIR values.
UP, DOWN, LEFT, RIGHT = "UP", "DOWN", "LEFT", "RIGHT"
# One step on the grid for each direction (row grows downward, col grows rightward).
DIRECTION_DELTAS = {UP: (-1, 0), DOWN: (1, 0), LEFT: (0, -1), RIGHT: (0, 1)}
