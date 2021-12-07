import numpy as np

pos = np.array([int(v) for v in open('input.txt').readline().split(',')])
print('part 1:', sum(abs(pos - np.median(pos))))
mean = np.mean(pos)
delta = abs(pos - round(mean + np.mean(np.sign(pos - mean)) / 2))
print('part 2:', sum(delta * (delta + 1) // 2))
