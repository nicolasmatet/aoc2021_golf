import re
from collections import defaultdict, namedtuple
from typing import List

Rule = namedtuple('Rule', ['condition', 'path'])


def lines():
    regex = re.compile("(\d+),(\d+) -> (\d+),(\d+)")
    for l in open("input.txt"):
        m = re.match(regex, l).groups()
        yield (int(m[0]), int(m[1])), (int(m[2]), int(m[3]))


def get_horizontal_path(start, end):
    return ((x, start[1]) for x in range(start[0], end[0] + 1))


def get_vertical_path(start, end):
    return ((start[0], y) for y in range(start[1], end[1] + 1))


def get_diag_up_path(start, end):
    return zip(range(start[0], end[0] + 1), range(start[1], end[1] + 1))


def get_diag_down_path(start, end):
    return zip(range(start[0], end[0] + 1), range(start[1], end[1] - 1, -1))


def get_path(start, end, rules: List[Rule]):
    if start[0] > end[0] or (start[0] == end[0] and start[1] > end[1]):
        end, start = start, end
    for rule in rules:
        if rule.condition(start, end):
            return rule.path(start, end)
    return []

horizontal = Rule(condition=lambda start, end: start[1] == end[1], path=get_horizontal_path)
vertical = Rule(condition=lambda start, end: start[0] == end[0], path=get_vertical_path)
diag_up = Rule(condition=lambda start, end: start[1] < end[1], path=get_diag_up_path)
diag_down = Rule(condition=lambda start, end: start[1] > end[1], path=get_diag_down_path)


def solve(rules):
    mapping = defaultdict(lambda: 0)
    for start, end in lines():
        for point in get_path(start, end, rules):
            mapping[point] += 1
    return len([v for v in mapping.values() if v > 1])


print(solve([horizontal, vertical]))  # part 1
print(solve([horizontal, vertical, diag_up, diag_down]))  # part 2
