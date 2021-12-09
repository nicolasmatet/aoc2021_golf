from collections import defaultdict
from functools import reduce
from itertools import count

import numpy as np


def lines():
    for l in open("input.txt"):
        yield [9, *(int(v) for v in l.strip()), 9]


def width():
    with open('input.txt') as f:
        return len(f.readline().strip())


def solve1():

    lowpoints = dict()
    previous_line = [9] * (width() + 2)
    for y, line in enumerate(lines()):
        y += 1
        for x, height in enumerate(line[1:-1]):
            x += 1
            lower_than_top = height < previous_line[x]
            lower_than_left = height < line[x - 1]
            if lower_than_left:
                if (pos_previous := (x - 1, y)) in lowpoints:
                    del lowpoints[pos_previous]
            if lower_than_top:
                if (pos_previous := (x, y - 1)) in lowpoints:
                    del lowpoints[pos_previous]
            if lower_than_top and lower_than_left:
                lowpoints[(x, y)] = height
        previous_line = line
    return sum(h + 1 for h in lowpoints.values())


class BassinMap:
    def __init__(self, heightmap):
        self.heightmap = heightmap
        self.bassinmap = np.zeros(shape=heightmap.shape)
        self.bassinsize = defaultdict(lambda: 0)
        self.bassin_ids = count(start=1)

    @staticmethod
    def neighbors(x, y):
        yield x - 1, y
        yield x + 1, y
        yield x, y - 1
        yield x, y + 1

    def create_from(self, x, y):
        self.extend_from(x, y, next(self.bassin_ids))

    def extend_from(self, x, y, nbassin):
        self.bassinsize[nbassin] += 1
        self.bassinmap[x, y] = nbassin
        for xn, yn in self.neighbors(x, y):
            if not self.is_in_bassin(xn, yn):
                self.extend_from(xn, yn, nbassin)

    def is_in_bassin(self, x, y):
        return self.heightmap[x, y] == 9 or self.bassinmap[x, y] != 0

    def sorted_sizes(self):
        return sorted(list(self.bassinsize.values()), reverse=True)


def solve2():
    w = width() + 2
    heightmap = np.array([[9] * w, *[line for line in lines()], [9] * w])
    bassinmap = BassinMap(heightmap)
    for x in range(heightmap.shape[0]):
        for y in range(heightmap.shape[1]):
            if not bassinmap.is_in_bassin(x, y):
                bassinmap.create_from(x, y)
    return reduce(lambda x, m: x * m, bassinmap.sorted_sizes()[0:3], 1)


print(solve1())
print(solve2())
