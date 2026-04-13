"""Start the window game. Run: python src/main.py   or   python src/main.py -f examples/level2.txt"""
from __future__ import annotations

import os
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> None:
    argv = sys.argv[1:] if argv is None else argv
    src = Path(__file__).resolve().parent
    if str(src) not in sys.path:
        sys.path.insert(0, str(src))
    import gui

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
