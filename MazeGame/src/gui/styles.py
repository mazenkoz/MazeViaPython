# Shared Tk button styling (colours match constants.UI_BTN_*).
# Centralised so welcome + maze screens stay visually consistent.
from __future__ import annotations

import tkinter as tk

from .constants import (
    UI_BTN_PRIMARY,
    UI_BTN_PRIMARY_ACTIVE,
    UI_BTN_SECONDARY,
    UI_BTN_SECONDARY_ACTIVE,
)


def style_primary_button(btn: tk.Button) -> None:
    """Blue style for main actions (Reset, Show path, unlocked levels)."""
    btn.configure(
        bg=UI_BTN_PRIMARY,
        fg="#ffffff",
        activebackground=UI_BTN_PRIMARY_ACTIVE,
        activeforeground="#ffffff",
        relief=tk.FLAT,
        padx=10,
        pady=5,
        cursor="hand2",
    )


def style_secondary_button(btn: tk.Button) -> None:
    """Grey style for Main menu, Next (before win), Quit."""
    btn.configure(
        bg=UI_BTN_SECONDARY,
        fg="#ffffff",
        activebackground=UI_BTN_SECONDARY_ACTIVE,
        activeforeground="#ffffff",
        relief=tk.FLAT,
        padx=10,
        pady=5,
        cursor="hand2",
    )
