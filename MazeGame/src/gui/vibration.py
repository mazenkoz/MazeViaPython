# Illegal-move feedback: short horizontal shake of everything drawn on the maze canvas.
# Only the maze canvas moves — easier to notice than shaking the whole window.
from __future__ import annotations

import tkinter as tk

# How far the canvas shifts left/right on each step (pixels), ending back at 0.
_SHAKE_OFFSETS = (0, 12, -12, 10, -10, 6, -6, 3, -3, 0)
# Milliseconds between steps so the eye can follow the motion.
_SHAKE_STEP_DELAY_MS = 28


def shake_canvas(
    canvas: tk.Canvas,
    offsets: tuple[int, ...] = _SHAKE_OFFSETS,
    delay_ms: int = _SHAKE_STEP_DELAY_MS,
) -> None:
    """
    Schedule several small horizontal moves on the canvas.

    If the player bumps a wall again before the animation finishes, we bump an internal
    “generation” counter so old scheduled steps do nothing — only the newest shake runs.
    """
    if not hasattr(canvas, "_shake_state"):
        canvas._shake_state = {"generation": 0, "offset_so_far": 0}  # type: ignore[attr-defined]
    state = canvas._shake_state  # type: ignore[attr-defined]

    state["generation"] += 1
    my_generation = state["generation"]
    state["offset_so_far"] = 0

    def apply_step(target_offset: int, generation_when_started: int) -> None:
        if generation_when_started != state["generation"]:
            return
        delta = target_offset - state["offset_so_far"]
        canvas.move("all", delta, 0)
        state["offset_so_far"] = target_offset

    for step_index, offset in enumerate(offsets):
        delay = step_index * delay_ms
        # Default args bind offset and generation now, so this is not the “loop lambda” bug.
        canvas.after(delay, lambda off=offset, gen=my_generation: apply_step(off, gen))
