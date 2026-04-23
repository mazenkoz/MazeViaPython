"""Unit tests for breadth-first pathfinding on maze grids.

Builds small in-memory layouts plus loads ``examples/level1.txt`` to ensure the
real on-disk format stays solvable. Imports ``maze_load`` / ``maze_play`` and the
``pathfinding`` module with ``src`` prepended to ``sys.path`` so ``python -m unittest``
works from the ``MazeGame`` directory without installing a package.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

_SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(_SRC))

from maze_load import find_start_goal, load_grid  # noqa: E402
from maze_play import is_walkable  # noqa: E402
from pathfinding import find_path  # noqa: E402


class TestPathfinding(unittest.TestCase):
    def test_corridor(self) -> None:
        g = [list("#####"), list("#S.G#"), list("#####")]
        path = find_path(g, (1, 1), (1, 3))
        self.assertIsNotNone(path)
        assert path is not None
        self.assertEqual(len(path), 3)
        self.assertEqual(path[0], (1, 1))
        self.assertEqual(path[-1], (1, 3))

    def test_blocked(self) -> None:
        g = [list("#####"), list("#S#G#"), list("#####")]
        self.assertIsNone(find_path(g, (1, 1), (1, 3)))

    def test_start_is_goal(self) -> None:
        g = [list("###"), list("#G#"), list("###")]
        self.assertEqual(find_path(g, (1, 1), (1, 1)), [(1, 1)])

    def test_path_walkable(self) -> None:
        g = [
            list("#######"),
            list("#S...G#"),
            list("#.###.#"),
            list("#.....#"),
            list("#######"),
        ]
        path = find_path(g, (1, 1), (1, 5))
        self.assertIsNotNone(path)
        assert path is not None
        for r, c in path:
            self.assertTrue(is_walkable(g, r, c))

    def test_level1_solvable(self) -> None:
        root = Path(__file__).resolve().parent.parent
        p = root / "examples" / "level1.txt"
        grid = load_grid(str(p))
        s, gl = find_start_goal(grid)
        self.assertIsNotNone(find_path(grid, s, gl))


if __name__ == "__main__":
    unittest.main()
