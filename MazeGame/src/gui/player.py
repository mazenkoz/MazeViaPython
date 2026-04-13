# Player sprite: pixel rectangle inside a grid cell on the canvas.
# Canvas (0,0) is top-left of the maze area; rows increase downward like the text file.
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
