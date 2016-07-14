from collections import namedtuple

ALIVE = '*'
EMPTY = '-'
TICK = object()

Query = namedtuple('Query', ('x', 'y'))
Transition = namedtuple('Transition', ('x', 'y', 'state'))


def count_neighbors(x, y):
    """Count number of live neighbors"""
    n_ = yield Query(x + 0, y + 1)  # North
    ne = yield Query(x + 1, y + 1)  # Northeast
    e_ = yield Query(x + 1, y + 0)  # East
    se = yield Query(x + 1, y - 1)  # Southeast
    s_ = yield Query(x + 0, y - 1)  # South
    sw = yield Query(x - 1, y - 1)  # Southwest
    w_ = yield Query(x - 1, y - 0)  # West
    nw = yield Query(x - 1, y - 1)  # Northwest

    neighbor_states = [n_, ne, e_, se, s_, sw, w_, nw]
    return sum(state == ALIVE for state in neighbor_states)


def game_logic(state, neighbors):
    """What to do  with state if we have given live neighbors"""
    if state == ALIVE:
        if neighbors < 2:
            return EMPTY  # Die: too few
        elif neighbors > 3:
            return EMPTY  # Die: too many
    else:
        if neighbors == 3:
            return ALIVE  # Regenerate
    return state


def step_cell(x, y):
    """Gets cell and transition it"""
    state = yield Query(x, y)
    neighbors = yield from count_neighbors(x, y)
    next_state = game_logic(state, neighbors)
    yield Transition(x, y, next_state)


def simulate(width, height):
    """Checks all cells for update"""
    while True:
        for x in range(width):
            for y in range(height):
                yield from step_cell(x, y)
        yield TICK


class Grid(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rows = []
        for _ in range(self.height):
            self.rows.append([EMPTY]*self.width)

    def __str__(self):
        return '\n'.join(''.join(row) for row in self.rows)

    def query(self, x, y):
        return self.rows[y % self.height][x % self.width]

    def assign(self, x, y, state):
        self.rows[y % self.height][x % self.width] = state


def live_a_generation(grid, sim):
    progeny = Grid(grid.width, grid.width)
    item = next(sim)  # Process all grid cells
    while item is not TICK:
        if isinstance(item, Query):
            state = grid.query(item.x, item.y)
            item = sim.send(state)
        else:
            progeny.assign(item.x, item.y, item.state)
            item = next(sim)
    return progeny


def main():
    grid = Grid(5, 9)
    grid.assign(0, 0, ALIVE)
    grid.assign(0, 1, ALIVE)
    sim = simulate(grid.width, grid.height)
    for _ in range(5):
        print(grid)
        grid = live_a_generation(grid, sim)

if __name__ == '__main__':
    main()
