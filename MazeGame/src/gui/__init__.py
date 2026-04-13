# Package entry: fix sys.path for non-package runs, then expose run_gui / MazeNavigatorApp.
# Typical use: from gui import run_gui — requires `src` on sys.path (main.py and this block ensure that).
from __future__ import annotations

import sys
from pathlib import Path

# Parent `src` must be on path so imports like `game_logic` resolve from this package.
_SRC_DIR = Path(__file__).resolve().parent.parent
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

import tkinter as tk

from .app import MazeNavigatorApp


def run_gui(grid_path: str | None = None) -> None:
    # Create root window, build app (welcome or direct maze), block until window closes.
    root = tk.Tk()
    MazeNavigatorApp(root, initial_grid_path=grid_path)
    # Tk event loop; processes clicks/keys/redraws until the user closes the window.
    root.mainloop()


__all__ = ["run_gui", "MazeNavigatorApp"]
