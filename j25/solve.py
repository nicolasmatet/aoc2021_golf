import numpy as np

EAST = 1
SOUTH = 0
EMPTY = -1


def lines():
    mapping = {'>': EAST, 'v': SOUTH}
    for line in open("input.txt"):
        yield [mapping[c] if c in mapping else EMPTY for c in line.strip()]


def pprint(map):
    mapping = {EAST: '>', SOUTH: 'v'}
    for line in map:
        print(''.join([mapping[c] if c in mapping else '.' for c in line]))
    print('-----------------')


def want_to_move(map, direction):
    return map == direction


def free_to_move(map, want_to_move, direction):
    return want_to_move & np.roll(map == EMPTY, -1, axis=direction)


def iterate(map):
    something_moved = False
    for direction in [EAST, SOUTH]:
        want = want_to_move(map, direction)
        will = free_to_move(map, want, direction)
        if np.any(will):
            something_moved = True
        map[np.roll(will, 1, axis=direction)] = direction
        map[will] = EMPTY
    return map, something_moved


def solve1():
    map = np.array([l for l in lines()])
    something_moved = True
    steps = 0
    while something_moved:
        # pprint(map)
        steps += 1
        map, something_moved = iterate(map)
    pprint(map)
    return steps


print(solve1())
