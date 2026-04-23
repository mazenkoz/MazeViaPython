# Single-level play screen: ``tk.Frame`` subclass that loads one maze file, owns keyboard focus,
# and wires canvas redraws to ``maze_render``. Uses ``maze_load`` / ``maze_play`` for the same
# rules as the terminal game; ``pathfinding.find_path`` paints optional yellow path tiles when asked.
#
# Binds WASD / arrows via ``constants.KEY_TO_DIR``, ``R`` reset, ``P`` path preview. On win,
# invokes optional ``on_level_completed`` / enables Next when part of the numbered campaign.
# Illegal moves call ``vibration.shake_canvas`` for quick feedback without changing layout.
from __future__ import annotations
import tkinter as tk
from tkinter import messagebox
from typing import Callable, List, Optional, Set, Tuple
from maze_load import find_start_goal, load_grid
from maze_play import check_win, move_player
from pathfinding import find_path
from .constants import CELL_PX, KEY_TO_DIR, UI_BG
from .levels import NUM_LEVELS
from .maze_play_ui import build_maze_play_ui
from .maze_render import draw_maze_layer, draw_player_on_maze
from .styles import style_primary_button, style_secondary_button
from .vibration import shake_canvas


class MazeGameFrame(tk.Frame):
    def __init__(
        self,
        master: tk.Widget,
        grid_path: str,
        on_menu: Callable[[], None],
        level_num: Optional[int] = None,
        on_level_completed: Optional[Callable[[int], None]] = None,
        on_next_level: Optional[Callable[[int], None]] = None,
    ) -> None:
        # takefocus=True so arrow keys are sent to this frame (not lost to the window).
        super().__init__(master, takefocus=True, bg=UI_BG)

        self.grid_path = grid_path
        self.on_menu = on_menu
        self.level_num = level_num
        self.on_level_completed = on_level_completed
        self.on_next_level = on_next_level

        # Use self.maze for the 2D list — not self.grid, because Frame.grid() is Tk’s layout method.
        self.maze: List[List[str]] = load_grid(grid_path)
        self.start_pos, self.goal_pos = find_start_goal(self.maze)
        self.player_pos: Tuple[int, int] = self.start_pos

        # When the user presses P, we store path cells here so redraw can paint them yellow.
        self.path_cells: Optional[Set[Tuple[int, int]]] = None

        row_count = len(self.maze)
        col_count = len(self.maze[0]) if self.maze else 0
        self.rows, self.cols = row_count, col_count

        self.won = False
        self.level_cleared = False

        self.canvas_w = self.cols * CELL_PX
        self.canvas_h = self.rows * CELL_PX

        ui = build_maze_play_ui(
            self,
            self.canvas_w,
            self.canvas_h,
            on_reset=self.reset_level,
            on_show_path=self.show_path,
            on_menu=self.on_menu,
            on_next=self._open_next_level,
        )
        self.canvas = ui.canvas
        self.status_label = ui.status_label
        self.btn_next = ui.btn_next

        self.bind("<Key>", self.on_key)
        # Wait until the window is visible, then grab keyboard focus for this frame.
        self.after(50, self.focus_set)
        self.redraw()

    def reset_level(self) -> None:
        self.maze = load_grid(self.grid_path)
        self.start_pos, self.goal_pos = find_start_goal(self.maze)
        self.player_pos = self.start_pos
        self.path_cells = None
        self.won = False
        self.level_cleared = False
        self.status_label.configure(text="")
        self.btn_next.configure(state=tk.DISABLED)
        style_secondary_button(self.btn_next)
        self.redraw()

    def show_path(self) -> None:
        if self.won:
            return
        path = find_path(self.maze, self.player_pos, self.goal_pos)
        if path is None:
            messagebox.showinfo("Path", "No path exists to the goal from here.")
            self.path_cells = None
        else:
            self.path_cells = set(path)
        self.redraw()

    def on_key(self, event: tk.Event) -> None:
        """Tk calls this for every key press while this frame has focus."""
        if self.won:
            return

        if _event_is_path_key(event):
            self.show_path()
            return

        if _event_is_reset_key(event):
            self.reset_level()
            return

        direction = _direction_from_key_event(event)
        if direction is None:
            return

        self._move_one_step(direction)

    def _move_one_step(self, direction: str) -> None:
        old_position = self.player_pos
        new_position = move_player(self.maze, self.player_pos, direction)

        if new_position == old_position:
            shake_canvas(self.canvas)
        else:
            self.player_pos = new_position
            self.path_cells = None

        self.redraw()

        if check_win(self.player_pos, self.goal_pos):
            self.won = True
            self.level_cleared = True
            if self.level_num is not None and self.on_level_completed is not None:
                self.on_level_completed(self.level_num)
            self._show_win_status()

    def _show_win_status(self) -> None:
        if self.level_num is None:
            self.status_label.configure(text="Level complete!")
        elif self.level_num < NUM_LEVELS:
            self.status_label.configure(text=f"Level {self.level_num} complete! Next level unlocked.")
            self.btn_next.configure(state=tk.NORMAL)
            style_primary_button(self.btn_next)
        else:
            self.status_label.configure(text="Final level complete! Great job.")

    def _open_next_level(self) -> None:
        if not self.level_cleared:
            return
        if self.level_num is None:
            return
        if self.level_num >= NUM_LEVELS:
            return
        if self.on_next_level is not None:
            next_level_number = self.level_num + 1
            self.on_next_level(next_level_number)

    def redraw(self) -> None:
        self.canvas.delete("all")
        path_for_draw: Set[Tuple[int, int]] = self.path_cells if self.path_cells is not None else set()
        draw_maze_layer(self.canvas, self.maze, path_for_draw)
        draw_player_on_maze(self.canvas, self.player_pos)


def _event_is_path_key(event: tk.Event) -> bool:
    return event.keysym in ("p", "P") or event.char in ("p", "P")


def _event_is_reset_key(event: tk.Event) -> bool:
    return event.keysym in ("r", "R") or event.char in ("r", "R")


def _direction_from_key_event(event: tk.Event) -> str | None:
    """Arrow keys use keysym; WASD often appears in event.char — KEY_TO_DIR covers both."""
    direction = KEY_TO_DIR.get(event.keysym)
    if direction is not None:
        return direction
    return KEY_TO_DIR.get(event.char)
