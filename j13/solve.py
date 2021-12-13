import re
import numpy as np

regex_fold = re.compile("([xy])=([0-9]+)")
fold_callbacks = {
    'x': lambda fold_position: lambda point: foldx(point, fold_position),
    'y': lambda fold_position: lambda point: foldy(point, fold_position)
}


def foldx(point, fold_position):
    if point[0] < fold_position:
        return point
    return 2 * fold_position - point[0], point[1]


def foldy(point, fold_position):
    if point[1] < fold_position:
        return point
    return point[0], 2 * fold_position - point[1]


def get_points(lines):
    while (line := next(lines).strip()) != '':
        x, y = line.split(',')
        yield int(x), int(y)


def get_folds(lines):
    for line in lines:
        direction, position = re.search(regex_fold, line).groups()
        yield fold_callbacks[direction](int(position))


def apply_fold(points, fold):
    return set([fold(point) for point in points])


def render(points):
    image = np.zeros(shape=(40, 6))
    for x, y in points:
        image[x, y] = 1
    text = []
    for line in image.transpose():
        text.append(''.join('\u2588' if pixel else ' ' for pixel in line))
    print('\n'.join(text))


with open('input.txt') as input:
    points = set(get_points(input))
    folds = get_folds(input)
    points = apply_fold(points, next(folds))
    print(len(points))  # part1
    for fold in folds:
        points = apply_fold(points, fold)
    render(points)  # part 2
