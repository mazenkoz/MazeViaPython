# Composes the in-game chrome: header strip, maze ``Canvas``, status label, and control row.
# Pure layout + widget construction; all behaviour lives in ``MazeGameFrame`` via callbacks
# passed into ``build_maze_play_ui`` (reset, show path, menu, next level).
#
# Returns a small ``MazePlayWidgets`` dataclass so the frame can hold typed references without
# a tangle of instance attributes. Styling uses ``styles`` helpers for consistent primary/secondary
# buttons next to ``constants`` colour tokens.
from __future__ import annotations
from .styles import style_primary_button, style_secondary_button
from dataclasses import dataclass
from typing import Callable

import tkinter as tk

from .constants import (
    COLOR_FLOOR,
    UI_BG,
    UI_BORDER,
    UI_HEADER,
    UI_PANEL,
    UI_TEXT,
    UI_TEXT_MUTED,
    COLOR_STATUS,
)

@dataclass(frozen=True)
class MazePlayWidgets:
    """The three widgets MazeGameFrame needs after the layout is built."""
    canvas: tk.Canvas
    status_label: tk.Label
    btn_next: tk.Button


def build_maze_play_ui(
    parent: tk.Widget,
    canvas_w: int,
    canvas_h: int,
    *,
    on_reset: Callable[[], None],
    on_show_path: Callable[[], None],
    on_menu: Callable[[], None],
    on_next: Callable[[], None],
) -> MazePlayWidgets:
    """Build the full play screen under parent and return canvas + labels + Next button."""
    outer = tk.Frame(parent, bg=UI_BG)
    outer.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)

    _build_play_header(outer, on_reset, on_show_path, on_menu)

    canvas, status_label, btn_next = _build_maze_card(outer, canvas_w, canvas_h, on_next)
    return MazePlayWidgets(canvas=canvas, status_label=status_label, btn_next=btn_next)


def _build_play_header(
    outer: tk.Frame,
    on_reset: Callable[[], None],
    on_show_path: Callable[[], None],
    on_menu: Callable[[], None],
) -> None:
    """Top bar: title, hint text, and action buttons."""
    header = tk.Frame(outer, bg=UI_HEADER, highlightbackground=UI_BORDER, highlightthickness=1)
    header.pack(fill=tk.X, pady=(0, 12))

    title = tk.Label(
        header,
        text="Maze Navigator",
        font=("Segoe UI", 18, "bold"),
        fg=UI_TEXT,
        bg=UI_HEADER,
    )
    title.pack(anchor=tk.W, padx=16, pady=(12, 4))

    row = tk.Frame(header, bg=UI_HEADER)
    row.pack(fill=tk.X, padx=16, pady=(0, 12))

    hint = tk.Label(
        row,
        text="WASD / arrows — move   |   P — shortest path   |   R — reset",
        font=("Segoe UI", 10),
        fg=UI_TEXT_MUTED,
        bg=UI_HEADER,
    )
    hint.pack(side=tk.LEFT, fill=tk.X, expand=True)

    button_bar = tk.Frame(row, bg=UI_HEADER)
    button_bar.pack(side=tk.RIGHT)

    reset_btn = tk.Button(button_bar, text="Reset", command=on_reset, font=("Segoe UI", 10))
    style_primary_button(reset_btn)
    reset_btn.pack(side=tk.LEFT, padx=4)

    path_btn = tk.Button(button_bar, text="Show path (BFS)", command=on_show_path, font=("Segoe UI", 10))
    style_primary_button(path_btn)
    path_btn.pack(side=tk.LEFT, padx=4)

    menu_btn = tk.Button(button_bar, text="Main menu", command=on_menu, font=("Segoe UI", 10))
    style_secondary_button(menu_btn)
    menu_btn.pack(side=tk.LEFT, padx=(4, 0))


def _build_maze_card(
    outer: tk.Frame,
    canvas_w: int,
    canvas_h: int,
    on_next: Callable[[], None],
) -> tuple[tk.Canvas, tk.Label, tk.Button]:
    """White card around the maze, status text, and Next level."""
    card = tk.Frame(outer, bg=UI_PANEL, highlightbackground=UI_BORDER, highlightthickness=1)
    card.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(
        card,
        width=canvas_w,
        height=canvas_h,
        bg=COLOR_FLOOR,
        highlightthickness=0,
        bd=0,
    )
    canvas.pack(padx=12, pady=12)

    status_label = tk.Label(
        card,
        text="",
        font=("Segoe UI", 10, "bold"),
        fg=COLOR_STATUS,
        bg=UI_PANEL,
    )
    status_label.pack(anchor=tk.W, padx=12, pady=(0, 8))

    footer = tk.Frame(card, bg=UI_PANEL)
    footer.pack(fill=tk.X, padx=12, pady=(0, 10))

    next_btn = tk.Button(
        footer,
        text="Next level",
        command=on_next,
        font=("Segoe UI", 10),
        state=tk.DISABLED,
    )
    style_secondary_button(next_btn)
    next_btn.pack(side=tk.RIGHT)

    return canvas, status_label, next_btn
