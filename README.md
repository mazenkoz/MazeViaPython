# Maze Navigator

Python maze game: move from **S** (start) to **G** (goal) on a 2D grid, with **terminal** and **Tkinter GUI** modes and **BFS** shortest-path hints. Core logic is shared between both interfaces; pathfinding uses **no third-party libraries**.

---

## Project layout

| Folder | Contents |
|--------|-----------|
| **`src/`** | Core game logic, pathfinding, and GUI (modules: `grid`, `maze_load`, `maze_play`, `pathfinding`, package `gui/`, launchers). |
| **`docs/`** | `docs.py` (terminal file summaries), `file_summaries.json`, and other project notes (e.g. `PROJECT_REPORT.md`). |
| **`tests/`** | Unit tests for `find_path`, grid loading, and movement. |
| **`examples/`** | Runnable maze files `level1.txt` … `level8.txt` (plain text grids). |

---

## Dependencies and installation

Uses **only the Python standard library**. There is **no `requirements.txt`** and nothing to install with **pip**.

- **Python 3.10+** recommended (type hints such as `list[str]`).
- **Tkinter** (GUI): included with official Python on **Windows** and **macOS**. On some **Linux** systems install **`python3-tk`** (e.g. `sudo apt install python3-tk` on Debian/Ubuntu).

### Which folder is the “project root”?

All run commands below expect your terminal’s **current directory** to be the folder that **directly contains** `src/`, `docs/`, `tests/`, and `examples/` (usually named **`MazeGame`**).

If you downloaded or unzipped the repo so it looks like this:

```text
MazeViaPython/
  MazeGame/
    src/
    examples/
    ...
```

then **open a terminal**, go into the inner project folder, then run the game:

```powershell
cd MazeGame
```

On **Windows**, if `python` is not found but the **Python launcher** works, use **`py`** instead (shown below).

---

## Quick start

| Mode | Command (Windows `py`) | Command (`python`) |
|------|------------------------|--------------------|
| **Text (terminal)** | `py src/text_game.py` | `python src/text_game.py` |
| **GUI** | `py src/main.py` | `python src/main.py` |
| **Tests** | `py -m unittest discover -s tests -p "test_*.py" -v` | `python -m unittest discover -s tests -p "test_*.py" -v` |

---

## File summaries (terminal)

Short **2–3 line** descriptions for files under **`MazeGame`** are stored in **`MazeGame/docs/file_summaries.json`**, keyed by relative paths such as `src/pathfinding.py` or `examples/level1.txt` (use **/** in keys). The CLI **`docs/docs.py`** prints that text; it does **not** scrape comments or docstrings from your source files.

From the **`MazeGame`** folder (after `cd MazeGame`):

```powershell
py docs/docs.py src/main.py
py docs/docs.py src/pathfinding.py
py docs/docs.py examples/level1.txt
py docs/docs.py tests/test_movement.py
```

If you add a new module or level file, append a matching key and summary string to **`file_summaries.json`**. If the path is not under `MazeGame` or has no entry, the script prints a short error to stderr and exits with a non-zero code.

---

## How to run the game

### Text (terminal) mode

From the project root (folder containing `src/`):

```powershell
py src/text_game.py
```

You should see something like: maze size and the path to the level, then the prompt **`>`** and instructions for controls. The maze uses **`#`** for walls and **`P`** for the player.

**Default maze:** `examples/level1.txt`. To load another file:

```powershell
py src/text_game.py examples/level3.txt
```

**Text controls**

| Key | Action |
|-----|--------|
| w / a / s / d | Move up / left / down / right (type one letter, press **Enter** each time) |
| p | Shortest path (route shown with `o`; `S`/`G` unchanged in the file) |
| q | Quit |

---

### GUI mode

```powershell
py src/main.py
```

Welcome screen and level picker. Open a file directly:

```powershell
py src/main.py -f examples/level2.txt
py src/main.py examples/level2.txt
```

From the `src` directory:

```powershell
cd src
py -m gui --file ../examples/level1.txt
```

**GUI controls:** **WASD** or **arrow keys** — move; **P** or **Show path (BFS)** — yellow path overlay; **R** or **Reset** — reload level.

**GUI colours**

| Element | Colour |
|---------|--------|
| Wall | Black |
| Floor | White |
| Start | Green |
| Goal | Red |
| Player | Blue |
| Path | Yellow |

---

## Pathfinding algorithm

Implementation: **`src/pathfinding.py`**, function **`find_path(grid, start, goal)`**.

**Algorithm:** **breadth-first search (BFS)** on the grid as a graph.

- Cells are nodes; edges go **up, down, left, right** to **walkable** cells (not `#`, inside bounds). **S** and **G** are walkable like floor.
- Each step has equal cost → **unweighted** graph.
- BFS expands in **layers by distance** from the start. The **first** time the goal is reached, the path has the **fewest steps** — a **shortest path**.
- If there is no route, the function returns **`None`**.

**Implementation note:** The queue holds `(cell, path_so_far)` for clarity on small mazes. Very large mazes could use a parent map instead to save memory.

---

## How the code is structured

| Area | Location | Role |
|------|-----------|------|
| Grid model | `src/grid.py` | Cell characters, dimensions, copy, text path overlay. |
| Directions | `src/directions.py` | Direction names and `(d_row, d_col)`; shared with GUI keymap. |
| Loading | `src/maze_load.py` | Read `.txt` mazes, rectangle check, one `S` and one `G`. |
| Movement / win | `src/maze_play.py` | `is_walkable`, `move_player`, `check_win`. |
| Pathfinding | `src/pathfinding.py` | BFS `find_path`. |
| File summaries | `docs/docs.py`, `docs/file_summaries.json` | Terminal: `py docs/docs.py <path>` prints a fixed short blurb per project file. |
| Text UI | `src/text_game.py`, `src/text_display.py` | Terminal loop and display helpers. |
| GUI | `src/gui/` | Tkinter: `app.py`, `maze_frame.py`, welcome screens, rendering, styles. |
| Launchers | `src/main.py`, `src/gui/__main__.py` | GUI entry points. |

---

## Tests

```powershell
py -m unittest discover -s tests -p "test_*.py" -v
```

(or `python -m unittest …` as in Quick start.)

Covers **`find_path`**, **`load_grid`** / validation, and **`move_player`** (walls, bounds, bundled levels).

---

## Example levels (`examples/`)

Ready to run:

```powershell
py src/text_game.py examples/level1.txt
py src/main.py -f examples/level5.txt
```

| File | Suggested use |
|------|----------------|
| `level1.txt` | **Easy** — default; good for learning controls. |
| `level2.txt` … `level4.txt` | **Medium** — GUI campaign levels 2–4. |
| `level5.txt` … `level8.txt` | **Harder** — later campaign levels. |

The GUI welcome screen maps **Level 1**–**8** to these files. You can still open any other valid `.txt` maze via `main.py` if you pass the path.

**Format:** rectangular grid; exactly one **`S`** and one **`G`**; **`#`** = wall, **`.`** = floor.

---

*Standard library only; GUI and text mode share `maze_load`, `maze_play`, `pathfinding`, and `grid`.*
