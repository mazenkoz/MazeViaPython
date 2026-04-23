# Tkinter GUI package entry: ensures the parent ``src`` directory is on ``sys.path`` when the
# package is imported from a script run as ``python src/main.py`` or similar non-package runs.
#
# Exposes ``run_gui`` (builds root window + ``MazeNavigatorApp`` and starts ``mainloop``) and
# re-exports ``MazeNavigatorApp`` for callers that embed the UI. Typical use: ``from gui import run_gui``.
#
# Parent ``src`` must precede this package on the path so sibling modules such as ``maze_load``,
# ``maze_play``, and ``pathfinding`` import correctly from inside ``gui.*``.
from __future__ import annotations

import sys
from pathlib import Path

# Parent `src` must be on path so sibling modules (maze_load, maze_play, pathfinding, …) resolve.
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
