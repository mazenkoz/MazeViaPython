# Read maze files from disk and validate exactly one S and one G.
# Used by GUI, text game, and tests — same rules everywhere.
from __future__ import annotations

from typing import List, Tuple

from grid import GOAL, START


def load_grid(file_path: str) -> List[List[str]]:
    # Parse text file to list[list[str]]; skip blank lines; require rectangle; validate S/G.
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    # Blank lines are ignored so editors can leave trailing newlines without breaking width checks.
    rows = [list(line) for line in lines if line != ""]
    if not rows:
        raise ValueError("Maze file is empty or has no data rows.")
    w = len(rows[0])
    for i, row in enumerate(rows):
        if len(row) != w:
            raise ValueError(f"Row {i} has length {len(row)}, expected {w} (rectangular grid).")
    # Ensures exactly one start and one goal (raises ValueError otherwise).
    find_start_goal(rows)
    return rows


def find_start_goal(grid: List[List[str]]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    # Return (start_rc, goal_rc); raises ValueError if S or G count is not exactly one each.
    starts: list[tuple[int, int]] = []
    goals: list[tuple[int, int]] = []
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == START:
                starts.append((r, c))
            elif cell == GOAL:
                goals.append((r, c))
    if len(starts) != 1:
        raise ValueError(f"Expected exactly one '{START}', found {len(starts)}.")
    if len(goals) != 1:
        raise ValueError(f"Expected exactly one '{GOAL}', found {len(goals)}.")
    return starts[0], goals[0]
