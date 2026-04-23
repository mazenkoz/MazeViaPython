# Player avatar drawing on the maze canvas: converts logical (row, col) to pixel rectangles.
# ``cell_rect`` returns canvas coordinates for a square cell given ``CELL_PX``; ``draw_player``
# insets a smaller filled rectangle so the token reads clearly on top of floor/start/goal tiles.
#
# Coordinate system matches the text files: origin top-left, rows downward. Colour defaults to
# ``constants.COLOR_PLAYER`` but stays overridable for tests or themes.
from __future__ import annotations

import tkinter as tk
from typing import Tuple

from .constants import COLOR_PLAYER


def cell_rect(row: int, col: int, cell_px: int) -> Tuple[int, int, int, int]:
    """Pixel box for one cell: (left, top, right, bottom). Canvas (0,0) is top-left."""
    x0 = col * cell_px
    y0 = row * cell_px
    return (x0, y0, x0 + cell_px, y0 + cell_px)


def draw_player(
    canvas: tk.Canvas,
    row: int,
    col: int,
    cell_px: int,
    color: str = COLOR_PLAYER,
    margin: int = 4,
) -> None:
    """Draw a filled rectangle inset from the cell edges so grid lines stay visible."""
    x0, y0, x1, y1 = cell_rect(row, col, cell_px)
    canvas.create_rectangle(
        x0 + margin,
        y0 + margin,
        x1 - margin,
        y1 - margin,
        fill=color,
        outline=color,
    )
