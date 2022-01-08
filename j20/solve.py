from typing import Dict


def neighbors(x, y):
    for xn in range(x - 1, x + 2, 1):
        for yn in range(y - 1, y + 2, 1):
            yield xn, yn


def get_algo(input_file):
    algo = next(input_file).strip()
    next(input_file)
    return [1 if c == "#" else 0 for c in algo]


def get_image(input_file):
    image = dict()
    xmain, xmax, ymin, ymax = -1, -1, -1, -1

    for x, line in enumerate(input_file):
        xmax += 1
        ymax = len(line.strip()) - 1
        for y, c in enumerate(line.strip()):
            image[(x, y)] = 1 if c == "#" else 0
    new_image = Image(image)
    new_image.set_bounds(-1, xmax + 1, -1, ymax + 1)
    return new_image


class Image:
    def __init__(self, image: Dict) -> None:
        self.image = image
        self.out_of_boud_value = 0
        self.xmin, self.xmax, self.ymin, self.ymax = 0, 0, 0, 0

    def __len__(self):
        return len(self.image)

    def set_bounds(self, xmin, xmax, ymin, ymax):
        self.xmin, self.xmax, self.ymin, self.ymax = xmin, xmax, ymin, ymax

    def get_pixel_patch_value(self, x, y):
        weight = 1
        value = 0

        for xn in range(x + 1, x - 2, -1):
            for yn in range(y + 1, y - 2, -1):
                value += weight * self.get_pixel_value(xn, yn)
                weight *= 2
        return value

    def get_pixel_value(self, x, y):
        return self.image.get((x, y), self.out_of_boud_value)

    def update_image_data(self, image_data: Dict, algo, x, y):
        neighbor_value = self.get_pixel_patch_value(x, y)
        image_data[(x, y)] = algo[neighbor_value]

    def propagate(self, algo):
        new_image_data = dict()
        for x in range(self.xmin, self.xmax + 1):
            for y in range(self.ymin, self.ymax + 1):
                self.update_image_data(new_image_data, algo, x, y)
        new_image = Image(new_image_data)
        new_image.out_of_boud_value = algo[-1] if self.out_of_boud_value else algo[0]
        new_image.set_bounds(self.xmin - 1, self.xmax + 1, self.ymin - 1, self.ymax + 1)
        return new_image

    def count_active(self):
        return len([v for v in self.image.values() if v])


def solve1():
    input_file = open("input.txt")
    algo = get_algo(input_file)
    image = get_image(input_file)
    for _ in range(2):
        image = image.propagate(algo)
    return image.count_active()


def solve2():
    input_file = open("input.txt")
    algo = get_algo(input_file)
    image = get_image(input_file)
    for _ in range(50):
        image = image.propagate(algo)
    return image.count_active()


# 10, 24, 35
# 5044, 5050, 18074
print(solve1())
print(solve2())
