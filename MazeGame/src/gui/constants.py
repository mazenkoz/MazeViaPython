# Colours, sizes, and keyboard map for the Tkinter UI (no game rules here).
# Game logic lives in game_logic / pathfinding; this file is presentation only.
from __future__ import annotations

from directions import DOWN, LEFT, RIGHT, UP

# Maze tile colours on the canvas (hex).
COLOR_WALL = "#000000"
COLOR_FLOOR = "#ffffff"
COLOR_START = "#2ecc71"
COLOR_GOAL = "#e74c3c"
COLOR_PLAYER = "#3498db"
COLOR_PATH = "#f1c40f"
# Width and height of one grid cell in pixels (maze size in px = cols*CELL_PX by rows*CELL_PX).
CELL_PX = 28

# Window chrome (backgrounds, buttons, typography).
UI_BG = "#f0f4f8"
UI_PANEL = "#ffffff"
UI_HEADER = "#e8eef3"
UI_TEXT = "#2c3e50"
UI_TEXT_MUTED = "#5d6d7e"
UI_BORDER = "#cfd9dd"
UI_BTN_PRIMARY = "#3498db"
UI_BTN_PRIMARY_ACTIVE = "#2980b9"
UI_BTN_SECONDARY = "#7f8c8d"
UI_BTN_SECONDARY_ACTIVE = "#636e72"
WINDOW_GEOMETRY = "720x620"
WINDOW_MINSIZE_W = 640
WINDOW_MINSIZE_H = 560

# Map keyboard input to direction names understood by game_logic.move_player().
# Arrow keys: Tk puts names like "Up" in event.keysym.
# WASD: often appears as a single letter in event.char — maze_frame checks both.
KEY_TO_DIR = {
    "w": UP,
    "W": UP,
    "Up": UP,
    "s": DOWN,
    "S": DOWN,
    "Down": DOWN,
    "a": LEFT,
    "A": LEFT,
    "Left": LEFT,
    "d": RIGHT,
    "D": RIGHT,
    "Right": RIGHT,
}
