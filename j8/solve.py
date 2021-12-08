from itertools import chain
from typing import List, Set


class Digit:

    def __init__(self, value: int, segments: str):
        self.value = value
        self.segments = {*segments}

    def __str__(self):
        return '{} ({:d})'.format(''.join(sorted(list(self.segments))), self.value)

    def could_decode(self, coded_digit: 'Digit', decoded_digits: List['DecodedDigits']):
        for decoded_digit in decoded_digits:
            coded_match_len = len(coded_digit.segments.intersection(decoded_digit.coded))
            decoded_match_len = len(self.segments.intersection(decoded_digit.decoded))
            if coded_match_len != decoded_match_len:
                return False
        return True

    def decode(self, all_digits: List['Digit'], decoded_digits: List['DecodedDigits']):
        decoded_candidates = [d for d in all_digits if d.could_decode(self, decoded_digits)]
        if len(decoded_candidates) == 1:
            return decoded_candidates[0]

    def is_decoded(self):
        return self.value >= 0


class DecodedDigits:
    def __init__(self, coded: Set[str], decoded: Set[str]):
        self.coded = coded
        self.decoded = decoded


class Display:
    all_digits = [Digit(0, 'abcefg'), Digit(1, 'cf'), Digit(2, 'acdeg'), Digit(3, 'acdfg'), Digit(4, 'bcdf'),
                  Digit(5, 'abdfg'), Digit(6, 'abdefg'), Digit(7, 'acf'), Digit(8, 'abcdefg'), Digit(9, 'abcdfg')]

    def __init__(self, input: List[str], output: List[str]):
        self.input = [Digit(-1, v) for v in input]
        self.output = [Digit(-1, v) for v in output]
        self.decoded_digits = [DecodedDigits({*'abcdefg'}, {*'abcdefg'})]

    def has_undecoded_input(self):
        return len([d for d in self.input if d.value < 0])

    def output_value(self):
        return sum(o.value * 10 ** p for p, o in enumerate(self.output[::-1]))

    def decode(self):
        for coded_digit in chain(self.input, self.output):
            if coded_digit.is_decoded():
                continue
            decoded_digit = coded_digit.decode(self.all_digits, self.decoded_digits)
            if decoded_digit:
                coded_digit.value = decoded_digit.value
                self.decoded_digits.append(DecodedDigits(coded_digit.segments, decoded_digit.segments))


def display_generator():
    with open("input.txt") as f:
        while True:
            try:
                input, output = next(f).split('|')
                yield Display(input.split(), output.split())
            except StopIteration:
                return


def part1():
    displays = [*display_generator()]
    for display in displays:
        display.decode()
    return sum(d.value in {1, 4, 7, 8} for display in displays for d in display.output)


def part2():
    displays = [*display_generator()]
    for display in displays:
        while display.has_undecoded_input():
            display.decode()
    return sum(display.output_value() for display in displays)


print(part1())
print(part2())
