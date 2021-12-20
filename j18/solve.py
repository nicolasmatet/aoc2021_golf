from typing import Iterator
import functools

STACK_OPEN = "["
STACK_CLOSE = "]"


def lines():
    for line in open("j18/input.txt"):
        yield parse_snail_number(iter(line.strip()))


class SnailNumber:
    def __init__(self, stack) -> None:
        self.stack = self.reduce(stack)

    def __add__(self, other):
        return SnailNumber([STACK_OPEN, *self.stack, *other.stack, STACK_CLOSE])

    def __str__(self):
        return self.sequence_to_string(iter(self.stack))

    def magnitude(self):
        return self.sequence_to_magnitude(iter(self.stack))

    @classmethod
    def increment_left(cls, start_index, value, stack):
        for i in range(start_index - 1, -1, -1):
            if not (stack[i] == STACK_OPEN) and not (stack[i] == STACK_CLOSE):
                stack[i] += value
                break

    @classmethod
    def increment_right(cls, start_index, value, stack):
        for i in range(start_index + 1, len(stack)):
            if not (stack[i] == STACK_OPEN) and not (stack[i] == STACK_CLOSE):
                stack[i] += value
                break

    @classmethod
    def explode(cls, stack):
        depth = -1
        for i, v in enumerate(stack):
            if v == STACK_OPEN:
                depth += 1
            elif v == STACK_CLOSE:
                depth -= 1
            if depth == 4:
                left_value = stack[i + 1]
                right_value = stack[i + 2]
                cls.increment_left(i + 1, left_value, stack)
                cls.increment_right(i + 2, right_value, stack)
                return [*stack[0:i], 0, *stack[i + 4 :]]
        return stack

    @classmethod
    def split(cls, stack):
        for i, v in enumerate(stack):
            if not (stack[i] == STACK_OPEN) and not (stack[i] == STACK_CLOSE) and v > 9:
                return [
                    *stack[0:i],
                    STACK_OPEN,
                    v // 2,
                    (v + 1) // 2,
                    STACK_CLOSE,
                    *stack[i + 1 :],
                ]
        return stack

    @classmethod
    def reduce(cls, stack):
        actions = [lambda stack: cls.explode(stack), lambda stack: cls.split(stack)]
        action_index = 0
        action_changed_something = [True, True]
        while any(action_changed_something):
            new_stack = actions[action_index](stack)
            has_changed = cls.stack_has_changed(stack, new_stack)
            if has_changed:
                action_index = 0
            else:
                action_index = (action_index + 1) % 2
            stack = new_stack
            action_changed_something[action_index] = has_changed
        return stack

    @classmethod
    def stack_has_changed(cls, old_stack, new_stack):
        return len(old_stack) != len(new_stack)

    @classmethod
    def sequence_to_magnitude(cls, sequence):
        next_char = next(sequence)
        while next_char == STACK_CLOSE:
            next_char = next(sequence)
        if next_char == STACK_OPEN:
            left = cls.sequence_to_magnitude(sequence)
            right = cls.sequence_to_magnitude(sequence)
            return 3 * left + 2 * right
        return next_char

    @classmethod
    def sequence_to_string(cls, sequence):
        next_char = next(sequence)
        while next_char == STACK_CLOSE:
            next_char = next(sequence)
        if next_char == STACK_OPEN:
            left = cls.sequence_to_string(sequence)
            right = cls.sequence_to_string(sequence)
            return "[{},{}]".format(left, right)
        return str(next_char)


def parse_snail_number(sequence: Iterator[str]):
    snail_stack = []
    while True:
        try:
            next_char = next(sequence)
        except StopIteration:
            break
        if next_char == "[":
            snail_stack.append(STACK_OPEN)
        if next_char.isdigit():
            number, next_char = get_number(next_char, sequence)
            snail_stack.append(number)
        if next_char == "]":
            snail_stack.append(STACK_CLOSE)
    return SnailNumber(snail_stack)


def get_number(first_char, sequence):
    all_chars = [first_char]
    while (next_char := next(sequence)).isdigit():
        all_chars.append(next_char)
    return int("".join(all_chars)), next_char


def solve1(snail_numbers):
    res = functools.reduce(lambda s1, s2: s1 + s2, snail_numbers)
    return res.magnitude()


def solve2(snail_numbers):
    maxi_magnitude = 0
    for i in range(len(snail_numbers)):
        for j in range(len(snail_numbers)):
            if i == j:
                continue
            magnitude = solve1([snail_numbers[i], snail_numbers[j]])
            maxi_magnitude = max(maxi_magnitude, magnitude)
    return maxi_magnitude


assert solve1(list(lines())) == 3691
assert solve2(list(lines())) == 4756
