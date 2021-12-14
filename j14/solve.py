from collections import defaultdict
from typing import Dict


def entries(file):
    for line in file:
        pair, product = line.strip().split(' -> ')
        yield pair, Polymer({product: 1}, {pair[0] + product: 1, product + pair[1]: 1})


def get_polymerisation(file):
    polymerisation = {pair: polymer for pair, polymer in entries(file)}
    for polymer in polymerisation.values():
        polymer.pairs = {pair: count for pair, count in polymer.pairs.items() if pair in polymerisation}
    return polymerisation


class Polymer:
    def __init__(self, content: Dict[str, int], pairs: Dict[str, int]):
        self.content = content
        self.pairs = pairs

    def __mul__(self, other):
        content = {base: count * other for base, count in self.content.items()}
        pairs = {pair: count * other for pair, count in self.pairs.items()}
        return Polymer(content, pairs)

    def __add__(self, other):
        content = defaultdict(lambda: 0, self.content)
        pairs = defaultdict(lambda: 0, self.pairs)
        for base, count_base in other.content.items():
            content[base] += count_base
        for pair, count_pair_new in other.pairs.items():
            pairs[pair] += count_pair_new
        return Polymer(content, pairs)

    def polymerise(self, polymerisation: Dict[str, 'Polymer']):
        polymer = Polymer(self.content, {})
        for pair, count_pair in self.pairs.items():
            polymer = polymer + polymerisation[pair] * count_pair
        return polymer

    def polymerise_up_to(self, polymerisation: Dict[str, 'Polymer'], limit: int) -> 'Polymer':
        polymer = self
        for i in range(limit):
            polymer = polymer.polymerise(polymerisation)
        return polymer

    def score(self):
        values = sorted(self.content.values())
        return values[-1] - values[0]

    @classmethod
    def count_content(cls, sequence):
        content = defaultdict(lambda: 0)
        for c in sequence:
            content[c] += 1
        return content

    @classmethod
    def count_pairs(cls, sequence: str, polymerisation: Dict[str, 'Polymer']):
        pairs = defaultdict(lambda: 0)
        for i in range(len(sequence) - 1):
            if (pair := sequence[i:i + 2]) in polymerisation:
                pairs[pair] += 1
        return pairs


def solve1(up_to):
    with open('input.txt') as file:
        start = next(file).strip()
        next(file)
        polymerisation = get_polymerisation(file)
        polymer = Polymer(Polymer.count_content(start), Polymer.count_pairs(start, polymerisation))
        polymer = polymer.polymerise_up_to(polymerisation, up_to)
        return polymer.score()


print(solve1(10))
print(solve1(40))
