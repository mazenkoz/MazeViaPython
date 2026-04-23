"""Print a short (2–3 line) summary for a file under the MazeGame project.

Summaries are maintained in `docs/file_summaries.json` keyed by paths like
`src/main.py` or `examples/level1.txt`. This avoids scraping comments or
docstrings from source files.

Usage (from `MazeGame`): `py docs/docs.py src/pathfinding.py`
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_DOCS_DIR = Path(__file__).resolve().parent
_ROOT = _DOCS_DIR.parent
_SUMMARIES_PATH = _DOCS_DIR / "file_summaries.json"


def _load_summaries() -> dict[str, str]:
    raw = _SUMMARIES_PATH.read_text(encoding="utf-8")
    if raw.startswith("\ufeff"):
        raw = raw[1:]
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("file_summaries.json must be a JSON object")
    out: dict[str, str] = {}
    for k, v in data.items():
        if isinstance(k, str) and isinstance(v, str):
            out[k.replace("\\", "/")] = v.strip()
    return out


def lookup_summary(project_root: Path, target: Path) -> str | None:
    summaries = _load_summaries()
    resolved = target.resolve()
    try:
        key = resolved.relative_to(project_root.resolve()).as_posix()
    except ValueError:
        return None
    return summaries.get(key)


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: py docs/docs.py <path-to-file-under-MazeGame>", file=sys.stderr)
        print("Prints 2–3 lines from docs/file_summaries.json (path keys use /).", file=sys.stderr)
        return 2
    target = Path(sys.argv[1])
    if not target.is_file():
        print(f"Not found: {target}", file=sys.stderr)
        return 1
    desc = lookup_summary(_ROOT, target)
    if not desc:
        try:
            rel = target.resolve().relative_to(_ROOT.resolve()).as_posix()
        except ValueError:
            print(
                f"Path must be inside {_ROOT}. "
                f"Then add a key to docs/file_summaries.json if missing.",
                file=sys.stderr,
            )
            return 1
        print(
            f"No summary for {rel}. Add a 2–3 line entry to docs/file_summaries.json.",
            file=sys.stderr,
        )
        return 1
    print(desc)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
