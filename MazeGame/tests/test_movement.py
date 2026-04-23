"""Unit tests for movement, walkability, and maze file loading invariants.

Covers ``move_player`` against walls and grid edges, ``is_walkable`` semantics,
``load_grid`` validation (rectangle, exactly one S/G), and a quick sweep that
``examples/level1.txt`` … ``level8.txt`` all parse. Uses the same ``src`` path
hack as ``test_pathfinding`` so imports match the flat student layout.
"""
from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

_SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(_SRC))

from directions import DOWN, LEFT, RIGHT, UP  # noqa: E402
from maze_load import find_start_goal, load_grid  # noqa: E402
from maze_play import is_walkable, move_player  # noqa: E402


class TestMovement(unittest.TestCase):
    def test_cannot_walk_into_wall(self) -> None:
        g = [list("###"), list("#S#"), list("###")]
        pos = (1, 1)
        for d in (UP, DOWN, LEFT, RIGHT):
            self.assertEqual(move_player(g, pos, d), pos)

    def test_walk_on_floor(self) -> None:
        g = [list("#####"), list("#S..#"), list("#####")]
        pos = (1, 1)
        pos = move_player(g, pos, RIGHT)
        self.assertEqual(pos, (1, 2))
        pos = move_player(g, pos, RIGHT)
        self.assertEqual(pos, (1, 3))

    def test_cannot_leave_grid(self) -> None:
        g = [list("#"), list("S"), list("#")]
        pos = (1, 0)
        self.assertEqual(move_player(g, pos, LEFT), pos)
        self.assertEqual(move_player(g, pos, RIGHT), pos)

    def test_load_level1(self) -> None:
        root = Path(__file__).resolve().parent.parent
        p = root / "examples" / "level1.txt"
        grid = load_grid(str(p))
        self.assertGreater(len(grid), 0)
        self.assertGreater(len(grid), 2)
        self.assertGreater(len(grid[0]), 2)
        s, gl = find_start_goal(grid)
        self.assertEqual(grid[s[0]][s[1]], "S")
        self.assertEqual(grid[gl[0]][gl[1]], "G")

    def test_rejects_two_starts(self) -> None:
        bad = "#####\n#SSG#\n#####\n"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
            f.write(bad)
            path = f.name
        try:
            with self.assertRaises(ValueError):
                load_grid(path)
        finally:
            os.unlink(path)

    def test_rejects_jagged(self) -> None:
        bad = "###\n##\n"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
            f.write(bad)
            path = f.name
        try:
            with self.assertRaises(ValueError):
                load_grid(path)
        finally:
            os.unlink(path)

    def test_goal_walkable(self) -> None:
        g = [list("#.#"), list("#G#"), list("#.#")]
        self.assertTrue(is_walkable(g, 1, 1))

    def test_levels_1_to_8(self) -> None:
        root = Path(__file__).resolve().parent.parent / "examples"
        for n in range(1, 9):
            p = root / f"level{n}.txt"
            self.assertTrue(p.is_file(), f"missing {p}")
            load_grid(str(p))


if __name__ == "__main__":
    unittest.main()
