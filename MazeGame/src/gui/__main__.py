# Allow ``python -m gui`` (with ``src`` on PYTHONPATH or run from layouts that treat ``gui`` as a
# package). Parses ``--file`` / ``-f`` with argparse; if the path is missing on disk we clear it
# and fall back to the welcome screen instead of hard-failing, mirroring ``src/main.py`` behaviour.
#
# Delegates window creation to ``gui.run_gui`` after resolving the optional maze path.
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
