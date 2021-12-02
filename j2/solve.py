def lines(p):
    for l in open(p):
        yield l[0], int(l[-2])


a = lambda m: lambda x, d, v: (x + (m == 0) * v, d + m * v)
inst = {'f': a(0), 'd': a(1), 'u': a(-1)}
x, d, x2, d2, a2 = (0,) * 5
for i, v in lines('input.txt'):
    x, d = inst[i](x, d, v)  # part1
    x2, a2, d2 = *inst[i](x2, a2, v), d2 if i != 'f' else d2 + v * a2  # part2
print(x * d)
print(x2 * d2)
