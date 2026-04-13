# BFS shortest path on the grid (unweighted; each step costs the same).
# For huge mazes you would store parent pointers instead of full paths in the queue.
from __future__ import annotations

from collections import deque
from typing import List, Optional, Tuple

from game_logic import is_walkable


def find_path(
    grid: List[List[str]],
    start: Tuple[int, int],
    goal: Tuple[int, int],
) -> Optional[List[Tuple[int, int]]]:
    # List of cells from start to goal inclusive, or None if unreachable.
    if start == goal:
        return [start]

    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    visited = {start}
    # Queue stores (cell, full path to that cell) — simple for small mazes.
    queue: deque = deque()
    queue.append((start, [start]))

    # Neighbour expansion order is fixed so equally-good paths tie-break the same way.
    neighbours = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        (r, c), path = queue.popleft()
        for dr, dc in neighbours:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            if not is_walkable(grid, nr, nc):
                continue
            nxt = (nr, nc)
            if nxt in visited:
                continue
            visited.add(nxt)
            new_path = path + [nxt]
            if nxt == goal:
                return new_path
            queue.append((nxt, new_path))

    # Exhausted search: goal is in another connected component (walls divide the maze).
    return None
