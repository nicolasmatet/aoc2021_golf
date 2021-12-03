import numpy as np

b = lambda a: int(''.join(str(d) for d in a), 2)
a = np.array([[int(d) for d in l.strip()] for l in open('input.txt').readlines()])
m = (a.sum(axis=0) >= len(a) / 2)
print(b(31 & m) * b(31 & ~m))  # part 1


def p2(c, d=lambda x, y: x == y, i=0):
    while len(c) > 1:
        m = (c[:, i].sum(axis=0) >= len(c) / 2)
        c = c[d(c[:, i], m), :]
        i += 1
    return b(c[0])
print(p2(a.copy()) * p2(a, lambda x, y: x != y))
