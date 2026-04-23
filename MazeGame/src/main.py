"""Graphical maze entrypoint for the project.

Ensures the `src` directory is on `sys.path` so `import gui` resolves when you run
`python src/main.py` from the `MazeGame` folder. Parses an optional maze file from the
command line (`-f` / `--file`, or a single path argument) and passes it to `gui.run_gui`,
which opens the Tk welcome screen or jumps straight into a custom level when the file exists.

Typical commands: `python src/main.py`, `python src/main.py -f examples/level2.txt`.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
import gui

def main(argv: list[str] | None = None) -> None:
    argv = sys.argv[1:] if argv is None else argv
    src = Path(__file__).resolve().parent
    if str(src) not in sys.path:
        sys.path.insert(0, str(src))
    

    fp: str | None = None
    if len(argv) >= 2 and argv[0] in ("-f", "--file"):
        fp = str(Path(argv[1]).resolve())
        if not os.path.isfile(fp):
            print(f"Not found: {fp}", file=sys.stderr)
            sys.exit(1)
    elif len(argv) == 1 and os.path.isfile(argv[0]):
        fp = str(Path(argv[0]).resolve())
    gui.run_gui(fp)


if __name__ == "__main__":
    main()
