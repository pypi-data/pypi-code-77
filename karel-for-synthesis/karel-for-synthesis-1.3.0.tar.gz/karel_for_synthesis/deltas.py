#   0: Hero facing North
#   1: Hero facing East
#   2: Hero facing South
#   3: Hero facing West
#   4: Internal walls
#   5: Surrounding walls
#   6: 1 marker
#   7: 2 markers
#   8: 3 markers
#   9: 4 markers
#   10: 5 markers
#   11: 6 markers
#   12: 7 markers
#   13: 8 markers
#   14: 9 markers
import numpy as np

SIZE = 18

HERO_DELTAS = [
    ("hero", i, x, y) for i in range(4) for x in range(SIZE) for y in range(SIZE)
]
WALL_DELTAS = [
    ("wall", which, i, x, y)
    for which in ("internal", "external")
    for i in range(2)
    for x in range(SIZE)
    for y in range(SIZE)
]
MARKER_DELTAS = [
    ("marker", i, x, y) for i in range(10) for x in range(SIZE) for y in range(SIZE)
]
STATE_DELTAS = HERO_DELTAS + MARKER_DELTAS
ALL_DELTAS = STATE_DELTAS + WALL_DELTAS


def compute_deltas(before, after):
    assert before.shape == after.shape == (15, SIZE, SIZE)
    before = before.copy()
    deltas = []
    if not (before[:4] == after[:4]).all():
        [[new_direction, x, y]] = np.array(np.where(after[:4])).T
        deltas.append(("hero", new_direction, x, y))
    for which, idx in ("internal", 4), ("external", 5):
        if not (before[idx] == after[idx]).all():
            for x, y in np.where((before[idx] == after[idx])).T:
                deltas.append(("wall", which, after[idx, x, y], x, y))
    for x, y in np.array(np.where((before[6:] != after[6:]).any(0))).T:
        new_value = after[6:, x, y].argmax() + 1 if after[6:, x, y].any() else 0
        deltas.append(("marker", new_value, x, y))
    return deltas


def apply_delta(delta, grid):
    if delta[0] == "hero":
        _, i, x, y = delta
        grid[:4] = 0
        grid[i, x, y] = 1
        return
    if delta[0] == "wall":
        _, which, i, x, y = delta
        channel = dict(internal=4, external=5)
        grid[channel, x, y] = i
        return
    if delta[0] == "marker":
        _, i, x, y = delta
        grid[6:, x, y] = 0
        if i > 0:
            grid[5 + i, x, y] = 1
        return
    raise RuntimeError(f"Invalid delta: {delta}")


def run_deltas(deltas, grid):
    grid = grid.copy()
    for delta in deltas:
        apply_delta(delta, grid)
    return grid
