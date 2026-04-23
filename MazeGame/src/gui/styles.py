# Small Tkinter button skin layer: primary (blue) and secondary (grey) presets used on the
# welcome screen and the in-game control bar. Colours and active states mirror ``constants.UI_BTN_*``
# and ``COLOR_FLOOR`` for readable white-on-blue labels.
#
# Keeping configuration here avoids duplicating ``relief``/``padx``/``pady`` tuples across frames
# when enabling/disabling the “Next level” action or styling level tiles.
from __future__ import annotations

import tkinter as tk

from .constants import (
    UI_BTN_PRIMARY,
    UI_BTN_PRIMARY_ACTIVE,
    UI_BTN_SECONDARY,
    UI_BTN_SECONDARY_ACTIVE,
    COLOR_FLOOR,
)


def style_primary_button(btn: tk.Button) -> None:
    """Blue style for main actions (Reset, Show path, unlocked levels)."""
    btn.configure(
        bg=UI_BTN_PRIMARY,
        fg=COLOR_FLOOR,
        activebackground=UI_BTN_PRIMARY_ACTIVE,
        activeforeground=COLOR_FLOOR,
        relief=tk.FLAT,
        padx=10,
        pady=5,
        cursor="hand2",
    )


def style_secondary_button(btn: tk.Button) -> None:
    """Grey style for Main menu, Next (before win), Quit."""
    btn.configure(
        bg=UI_BTN_SECONDARY,
        fg=COLOR_FLOOR,
        activebackground=UI_BTN_SECONDARY_ACTIVE,
        activeforeground=COLOR_FLOOR,
        relief=tk.FLAT,
        padx=10,
        pady=5,
        cursor="hand2",
    )
