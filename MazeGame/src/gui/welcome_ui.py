# Welcome screen layout pieces (header, level grid, help text, quit) — no app logic.
# WelcomeFrame passes callbacks and progression numbers in; this module only packs widgets.
from __future__ import annotations

import tkinter as tk
from tkinter import scrolledtext
from typing import Callable, Set

from .constants import UI_BG, UI_BORDER, UI_HEADER, UI_PANEL, UI_TEXT, UI_TEXT_MUTED
from .help_text import INSTRUCTIONS_TEXT
from .styles import style_primary_button, style_secondary_button


def pack_welcome_shell(host: tk.Widget) -> tk.Widget:
    """Outer padding + header + white card. Returns the card so callers can pack more into it."""
    outer = tk.Frame(host, bg=UI_BG)
    outer.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)

    header = tk.Frame(outer, bg=UI_HEADER, highlightbackground=UI_BORDER, highlightthickness=1)
    header.pack(fill=tk.X, pady=(0, 12))

    tk.Label(
        header,
        text="Maze Navigator",
        font=("Segoe UI", 18, "bold"),
        fg=UI_TEXT,
        bg=UI_HEADER,
    ).pack(pady=(12, 4))

    tk.Label(
        header,
        text="Welcome — pick a level to begin",
        font=("Segoe UI", 11),
        fg=UI_TEXT_MUTED,
        bg=UI_HEADER,
    ).pack(pady=(0, 12))

    card = tk.Frame(outer, bg=UI_PANEL, highlightbackground=UI_BORDER, highlightthickness=1)
    card.pack(fill=tk.BOTH, expand=True)
    return card


def pack_level_buttons(card: tk.Widget, unlocked: int, completed: Set[int], choose: Callable[[int], None]) -> None:
    """Eight buttons in two rows. Locked levels are greyed out; finished levels show a checkmark."""
    tk.Label(card, text="Levels", font=("Segoe UI", 11, "bold"), fg=UI_TEXT, bg=UI_PANEL).pack(pady=(16, 6))

    button_area = tk.Frame(card, bg=UI_PANEL)
    button_area.pack(pady=(0, 8))

    for row_index in range(2):
        row_frame = tk.Frame(button_area, bg=UI_PANEL)
        row_frame.pack()

        for col_index in range(4):
            level_number = row_index * 4 + col_index + 1
            _add_one_level_button(row_frame, col_index, level_number, unlocked, completed, choose)


def _add_one_level_button(
    row_frame: tk.Frame,
    column_index: int,
    level_number: int,
    unlocked_through: int,
    completed_levels: Set[int],
    choose: Callable[[int], None],
) -> None:
    # `lv=level_number` fixes a common bug: a bare `lambda: choose(level_number)` in a loop
    # would use the last value of level_number for every button. Default argument binds now.
    command = lambda lv=level_number: choose(lv)
    button = tk.Button(
        row_frame,
        text=f"Level {level_number}",
        width=10,
        font=("Segoe UI", 10),
        command=command,
    )

    is_unlocked = level_number <= unlocked_through
    if is_unlocked:
        label = f"Level {level_number}"
        if level_number in completed_levels:
            label = label + " ✓"
        button.configure(text=label)
        style_primary_button(button)
    else:
        button.configure(
            text=f"Level {level_number} 🔒",
            state=tk.DISABLED,
            bg="#dfe6e9",
            fg="#95a5a6",
            disabledforeground="#95a5a6",
            relief=tk.FLAT,
            padx=10,
            pady=5,
        )

    button.grid(row=0, column=column_index, padx=6, pady=6)


def pack_welcome_help(card: tk.Widget) -> None:
    """Read-only scroll box so long instructions still fit on small windows."""
    box = scrolledtext.ScrolledText(
        card,
        height=9,
        width=64,
        font=("Segoe UI", 10),
        wrap=tk.WORD,
        fg=UI_TEXT,
        bg=UI_PANEL,
        relief=tk.FLAT,
        highlightthickness=1,
        highlightbackground=UI_BORDER,
        padx=8,
        pady=8,
    )
    box.insert("1.0", INSTRUCTIONS_TEXT)
    box.tag_configure("center", justify="center")
    box.tag_add("center", "1.0", "end")
    box.configure(state=tk.DISABLED)
    box.pack(fill=tk.BOTH, expand=True, padx=20, pady=(12, 8))


def pack_quit_button(card: tk.Widget, on_quit: Callable[[], None]) -> None:
    quit_btn = tk.Button(card, text="Quit", font=("Segoe UI", 10), command=on_quit)
    style_secondary_button(quit_btn)
    quit_btn.pack(pady=(4, 16))
