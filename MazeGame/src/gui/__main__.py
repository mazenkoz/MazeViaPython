# Run the GUI as a module: from the project folder, `python -m gui` or `python -m gui -f path/to/maze.txt`.
# argparse adds --help automatically; file handling matches src/main.py.
from __future__ import annotations

import argparse
from pathlib import Path

from . import run_gui

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Maze Navigator GUI")
    parser.add_argument(
        "--file",
        "-f",
        default=None,
        help="Optional maze file (skips welcome menu if the file exists)",
    )
    args = parser.parse_args()
    fp = args.file
    if fp:
        fp = str(Path(fp).resolve())
        # Missing file: fall back to welcome instead of exiting with an error.
        if not Path(fp).is_file():
            fp = None
    run_gui(fp)
