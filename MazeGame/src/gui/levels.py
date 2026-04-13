# Paths to bundled examples/level1.txt … level8.txt and filename → level number.
# EXAMPLES_DIR is resolved from this file’s location so it works regardless of cwd.
from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

# This file is gui/levels.py → project root → examples/
EXAMPLES_DIR = Path(__file__).resolve().parent.parent.parent / "examples"
NUM_LEVELS = 8


def level_path(level_num: int) -> Path:
    """Return the full path to examples/level{n}.txt for n between 1 and NUM_LEVELS."""
    if not 1 <= level_num <= NUM_LEVELS:
        raise ValueError(f"Level must be 1–{NUM_LEVELS}, got {level_num}")
    return EXAMPLES_DIR / f"level{level_num}.txt"


def level_num_from_path(path: str | Path) -> Optional[int]:
    """
    If the file is named levelN.txt (campaign file), return N.
    Otherwise return None — custom filenames still work; we just skip “next level” campaign logic.
    """
    filename = Path(path).name
    pattern = r"level(\d+)\.txt"
    match = re.fullmatch(pattern, filename, flags=re.IGNORECASE)
    if match is None:
        return None

    n = int(match.group(1))
    if 1 <= n <= NUM_LEVELS:
        return n
    return None
