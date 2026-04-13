"""Play in the terminal: type wasd / p / q and press Enter after each command."""
from __future__ import annotations

import os
import sys
from pathlib import Path

_src = Path(__file__).resolve().parent
if str(_src) not in sys.path:
    sys.path.insert(0, str(_src))

from game_logic import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    check_win,
    find_start_goal,
    load_grid,
    move_player,
)
from pathfinding import find_path
from text_display import build_display, default_level_path, format_grid_lines, print_help


def main_path() -> str:
    return sys.argv[1] if len(sys.argv) > 1 else default_level_path()


def run(path: str) -> None:
    grid = load_grid(path)
    start, goal = find_start_goal(grid)
    player = start
    path_hint: list[tuple[int, int]] | None = None
    rows, cols = len(grid), len(grid[0])
    print(f"Maze {rows}x{cols}: {path}")
    print_help()

    while True:
        print()
        print(format_grid_lines(build_display(grid, player, path_hint)))
        if check_win(player, goal):
            print("\nYou reached the goal!\n")
            break
        try:
            cmd = input("> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("Bye.")
            break
        if cmd == "q":
            break
        if cmd == "p":
            p = find_path(grid, player, goal)
            if p is None:
                print("No path.")
                path_hint = None
            else:
                path_hint = p
                print(f"Path length: {len(p)} steps.")
            continue
        if len(cmd) != 1:
            print("One letter.")
            continue
        keys = {"w": UP, "s": DOWN, "a": LEFT, "d": RIGHT}
        if cmd not in keys:
            print("Use wasd, p, or q.")
            continue
        path_hint = None
        player = move_player(grid, player, keys[cmd])


if __name__ == "__main__":
    p = main_path()
    if not os.path.isfile(p):
        print(f"File not found: {p}", file=sys.stderr)
        sys.exit(1)
    run(p)
