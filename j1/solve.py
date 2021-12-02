l = [int(v) for v in open('input.txt').readlines()]
print(sum([u > v for u, v in zip(l[1:], l[:-1])]))  # part 1
print(sum([u > v for u, v in zip(l[3:], l[:-3])]))  # part 2
