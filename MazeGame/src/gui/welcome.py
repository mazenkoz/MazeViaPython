# Welcome / level picker frame; delegates layout to welcome_ui helpers.
# Wires app callbacks: on_select_level opens a maze; on_quit closes the whole program.
from __future__ import annotations

import tkinter as tk
from tkinter import messagebox
from typing import Callable, Set

from .constants import UI_BG
from .levels import level_path
from .welcome_ui import pack_level_buttons, pack_quit_button, pack_welcome_help, pack_welcome_shell


class WelcomeFrame(tk.Frame):
    def __init__(
        self,
        master: tk.Widget,
        on_select_level: Callable[[int], None],
        on_quit: Callable[[], None],
        unlocked_through: int,
        completed_levels: Set[int],
    ) -> None:
        super().__init__(master, bg=UI_BG)

        self.on_select_level = on_select_level
        self.on_quit = on_quit
        self.unlocked_through = unlocked_through
        self.completed_levels = completed_levels

        card = pack_welcome_shell(self)
        pack_level_buttons(card, self.unlocked_through, self.completed_levels, self._choose_level)
        pack_welcome_help(card)
        pack_quit_button(card, self.on_quit)

    def _choose_level(self, level_num: int) -> None:
        path = level_path(level_num)
        if not path.is_file():
            messagebox.showerror("Missing level", f"Could not find:\n{path}")
            return
        self.on_select_level(level_num)
