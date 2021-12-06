def init():
    with open("input.txt") as f:
        input = [int(v) for v in next(f).split(',')]
        school = [0] * 9
        for n in input:
            school[n] += 1
    return school


def spawn(school):
    spawning = school[0]
    school[0:-1] = school[1:]
    school[-1] = spawning
    school[6] += spawning


def solve(days):
    school = init()
    for _ in range(days):
        spawn(school)
    return sum(school)


print(solve(80))
print(solve(256))
