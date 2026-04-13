# Direction names and (d_row, d_col) steps; shared by GUI keymap and move_player().
# Keeping names as strings avoids mixing with Tk key names and makes logs readable.
from __future__ import annotations

# Strings passed into move_player; must match gui.constants.KEY_TO_DIR values.
UP, DOWN, LEFT, RIGHT = "UP", "DOWN", "LEFT", "RIGHT"
# One step on the grid for each direction (row grows downward, col grows rightward).
DIRECTION_DELTAS = {UP: (-1, 0), DOWN: (1, 0), LEFT: (0, -1), RIGHT: (0, 1)}
