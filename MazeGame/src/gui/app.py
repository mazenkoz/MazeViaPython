# Root window: swaps between welcome screen and maze screen; tracks level unlocks.
# Only this class ties together “campaign” progress; MazeGameFrame just reports wins via callbacks.
from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import messagebox
from typing import Set

from .constants import UI_BG, WINDOW_GEOMETRY, WINDOW_MINSIZE_H, WINDOW_MINSIZE_W
from .levels import NUM_LEVELS, level_num_from_path, level_path
from .maze_frame import MazeGameFrame
from .welcome import WelcomeFrame


class MazeNavigatorApp:
    def __init__(self, root: tk.Tk, initial_grid_path: str | None = None) -> None:
        self.root = root
        self.root.title("Maze Navigator")
        self.root.configure(bg=UI_BG)
        self.root.geometry(WINDOW_GEOMETRY)
        self.root.minsize(WINDOW_MINSIZE_W, WINDOW_MINSIZE_H)

        # One area for the whole UI; we destroy its children when switching welcome ↔ game.
        self.container = tk.Frame(root, bg=UI_BG)
        self.container.pack(fill=tk.BOTH, expand=True)

        self.completed_levels: Set[int] = set()
        # Player can open levels 1 through unlocked_through; higher numbers stay locked.
        self.unlocked_through = 1

        self._show_first_screen(initial_grid_path)

    def _show_first_screen(self, initial_grid_path: str | None) -> None:
        """Either open a maze file from the command line, or show the welcome menu."""
        if initial_grid_path is None:
            self.show_welcome()
            return

        path = Path(initial_grid_path)
        if not path.is_file():
            self.show_welcome()
            return

        level_number = level_num_from_path(initial_grid_path)
        if level_number is not None and level_number > self.unlocked_through:
            messagebox.showinfo(
                "Level locked",
                "That level is locked. Solve previous levels first.",
            )
            self.show_welcome()
            return

        self.show_game(str(path.resolve()))

    def clear_container(self) -> None:
        for child in self.container.winfo_children():
            child.destroy()

    def show_welcome(self) -> None:
        self.clear_container()
        welcome = WelcomeFrame(
            self.container,
            on_select_level=self._on_level_chosen,
            on_quit=self.root.destroy,
            unlocked_through=self.unlocked_through,
            completed_levels=self.completed_levels,
        )
        welcome.pack(fill=tk.BOTH, expand=True)

    def _on_level_chosen(self, level_num: int) -> None:
        if level_num > self.unlocked_through:
            messagebox.showinfo(
                "Level locked",
                f"Level {level_num} is locked. "
                f"Solve level {level_num - 1} first.",
            )
            return
        path = level_path(level_num)
        self.show_game(str(path))

    def _on_level_completed(self, level_num: int) -> None:
        self.completed_levels.add(level_num)
        beat_current_frontier = level_num == self.unlocked_through
        more_levels_exist = self.unlocked_through < NUM_LEVELS
        if beat_current_frontier and more_levels_exist:
            self.unlocked_through += 1

    def _on_next_level(self, level_num: int) -> None:
        if level_num > self.unlocked_through:
            return
        path = level_path(level_num)
        self.show_game(str(path))

    def show_game(self, grid_path: str) -> None:
        self.clear_container()
        if not Path(grid_path).is_file():
            messagebox.showerror("Error", f"File not found:\n{grid_path}")
            self.show_welcome()
            return

        level_num = level_num_from_path(grid_path)
        try:
            game = MazeGameFrame(
                self.container,
                grid_path,
                on_menu=self.show_welcome,
                level_num=level_num,
                on_level_completed=self._on_level_completed,
                on_next_level=self._on_next_level,
            )
        except ValueError as exc:
            messagebox.showerror("Invalid level", str(exc))
            self.show_welcome()
            return
        game.pack(fill=tk.BOTH, expand=True)
