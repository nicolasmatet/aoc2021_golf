import numpy as np


def neighbors(x, y, shape):
    nx, ny = shape
    nx -= 1
    ny -= 1
    if 0 < x < nx and 0 < y < ny:
        return np.array([x - 1, x - 1, x - 1, x, x, x + 1, x + 1, x + 1]), \
               np.array([y - 1, y, y + 1, y - 1, y + 1, y - 1, y, y + 1])

    if x == 0 and y < ny:
        return np.array([0, 1, 1, 1, 0]), np.array([y - 1, y - 1, y, y + 1, y + 1])
    if x < nx and y == ny:
        return np.array([x - 1, x - 1, x, x + 1, x + 1]), np.array([y, y - 1, y - 1, y - 1, y])
    if x == nx and y < ny:
        return np.array([x - 1, x - 1, x, x + 1, x + 1]), np.array([y, y - 1, y - 1, y - 1, y])
    if x < nx and y == 0:
        return np.array([x - 1, x - 1, x, x + 1, x + 1]), np.array([y, y + 1, y + 1, y + 1, y])

    if x == 0 and y == 0:
        return np.array([1, 1, 0]), np.array([0, 1, 1])
    if x == 0 and y == ny:
        return np.array([0, 1, 1]), np.array([y - 1, y - 1, y])
    if x == nx and y == ny:
        return np.array([x - 1, x - 1, x]), np.array([y, y - 1, y - 1])
    if x == nx and y == 0:
        return np.array([x - 1, x - 1, x]), np.array([y, y + 1, y + 1])
    raise ValueError('invalid indexes')
