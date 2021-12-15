from collections import namedtuple
import numpy as np
from queue import PriorityQueue


def lines():
    for line in open("input.txt"):
        yield [int(i) for i in line.strip()]


Point = namedtuple('Point', ['x', 'y', 'cost'])


class Map:
    def __init__(self, costs: np.array):
        self.costs = costs
        self.shape = costs.shape
        self.mean = np.mean(costs)
        self.total_costs1 = np.zeros(self.costs.shape)
        self.total_costs2 = np.zeros(self.costs.shape)

    def shape(self):
        return self.costs.shape()

    def neighbors(self, x, y):
        xm, ym = self.shape
        if x > 0:
            yield x - 1, y
        if x < xm - 1:
            yield x + 1, y
        if y > 0:
            yield x, y - 1
        if y < ym - 1:
            yield x, y + 1


class Queue:
    def __init__(self, size=0):
        self.queue = PriorityQueue(size)
        self.points_finder = {}

    def insert(self, point: Point):
        pos = (point.x, point.y)
        if pos in self.points_finder:
            self.remove(pos)
        entry = (point.cost, point)
        self.points_finder[pos] = entry
        self.queue.put(entry)

    def remove(self, pos):
        entry = self.points_finder[pos]
        entry[-1] = None
        del self.points_finder[pos]

    def validate(self, point):
        pos = (point.x, point.y)
        if pos not in self.points_finder:
            return True
        cost, point = self.points_finder[pos]
        return point.cost < cost

    def pop(self):
        while not self.queue.empty():
            cost, point = self.queue.get()
            if point:
                pos = (point.x, point.y)
                del self.points_finder[pos]
                return point
        raise KeyError('pop from an empty priority queue')


def djk_sym(start1: Point, start2: Point, map, queue1, queue2):
    while True:
        next_point(start1, map, queue1)
        if map.total_costs2[start1.x, start1.y] > 0:
            return start1.cost + map.total_costs2[start1.x, start1.y] - map.costs[start1.x, start1.y]
        map.total_costs1[start1.x, start1.y] = start1.cost

        start2 = next_point(start2, map, queue2)
        if map.total_costs1[start2.x, start2.y] > 0:
            return start2.cost + map.total_costs1[start2.x, start2.y] - map.costs[start2.x, start2.y]
        map.total_costs2[start2.x, start2.y] = start2.cost


def next_point(start, map, queue):
    for xn, yn in map.neighbors(start.x, start.y):
        if map.total_costs1[xn, yn] or map.total_costs2[xn, yn]:
            continue
        cost = start.cost + map.costs[xn, yn]
        neighbor = Point(x=xn, y=yn, cost=cost)
        if queue.validate(neighbor):
            queue.insert(neighbor)
    return queue.pop()


def lowest_cost(map):
    start = Point(x=0, y=0, cost=0)
    xe, ye = map.shape[0] - 1, map.shape[1] - 1
    end = Point(x=xe, y=ye, cost=map.costs[xe, ye])
    queue1 = Queue(map.shape[0] * map.shape[1])
    queue2 = Queue(map.shape[0] * map.shape[1])
    cost = djk_sym(start, end, map, queue1, queue2)
    return cost


def solve1():
    small_map = np.array([row for row in lines()])
    map = Map(small_map)
    return lowest_cost(map)


def solve2():
    small_map = np.array([row for row in lines()]) - 1
    repeat_x = np.concatenate([(small_map + i) % 9 for i in range(5)])
    big_map = np.concatenate([(repeat_x + i) % 9 for i in range(5)], axis=1) + 1
    map = Map(big_map)
    return lowest_cost(map)


print(solve1())
print(solve2())
