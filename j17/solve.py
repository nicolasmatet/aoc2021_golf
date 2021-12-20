xmin, xmax = 240, 292
ymin, ymax = -90, -57

def hit(vx, vy):
    x, y = 0, 0
    while x <= xmax and y >= ymin:
        if x >= xmin and y <= ymax:
            return True
        x += vx
        y += vy
        vx = vx - 1 if vx else 0
        vy = vy - 1


def solve1():
    max_height = 0
    for vx in range(xmax):
        for vy in range(xmax):
            if hit(vx, vy):
                height = vy * (vy + 1) / 2
                max_height = max(height, max_height)
    return max_height

def solve2():
    hits = 0
    for vx in range(xmax+1):
        for vy in range(ymin-1, xmax+1):
            if hit(vx, vy):
                hits+=1
    return hits

print(solve1())
print(solve2())