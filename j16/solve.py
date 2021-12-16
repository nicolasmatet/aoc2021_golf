import abc
from functools import reduce
from typing import Iterable


class BinStream:
    def __init__(self, hex_stream: Iterable):
        self._hex_stream = iter(hex_stream)
        self.bin_stream = self._all(self._hex_stream)

    @classmethod
    def bin_digits(cls, hex_digit):
        i = int(hex_digit, 16)
        digits = []
        for _ in range(4):
            digits.append(i % 2)
            i = i >> 1
        return reversed(digits)

    @classmethod
    def to_int(cls, bin_digits):
        small_endian = reversed([d for d in bin_digits])
        weight = 1
        res = 0
        for d in small_endian:
            res += weight * d
            weight *= 2
        return res

    def _all(self, hex_stream):
        for hex_digit in hex_stream:
            for bin_digit in self.bin_digits(hex_digit):
                yield bin_digit

    def next(self, n: int):
        for _ in range(n):
            yield next(self.bin_stream)

    def next_as_int(self, n: int = 1):
        return self.to_int(self.next(n))


class Paquet(abc.ABC):
    def __init__(self, version, paquet_type):
        self.length = 6
        self.version = version
        self.paquet_type = paquet_type
        self.successors = None
        self.value = None

    @abc.abstractmethod
    def parse(self, bin_stream: BinStream):
        pass

    @abc.abstractmethod
    def evaluate(self) -> int:
        pass

    @classmethod
    def parse_paquet_hierarchy(cls, bin_stream: BinStream) -> 'Paquet':
        version = bin_stream.next_as_int(3)
        paquet_type = bin_stream.next_as_int(3)
        if paquet_type == 4:
            paquet = LiteralPaquet(version, paquet_type)
            paquet.value = paquet.parse(bin_stream)
        else:
            paquet = OperatorPaquet(version, paquet_type)
            paquet.successors = paquet.parse(bin_stream)
        return paquet

    def sum_versions(self):
        if self.successors:
            return self.version + sum(succ.sum_versions() for succ in self.successors)
        return self.version


class LiteralPaquet(Paquet):
    def __init__(self, version, paquet_type):
        super().__init__(version, paquet_type)

    def parse(self, bin_stream: BinStream):
        is_continued = bin_stream.next_as_int()
        content = []
        while is_continued:
            content.extend(bin_stream.next(4))
            self.length += 5
            is_continued = bin_stream.next_as_int()
        content.extend(bin_stream.next(4))
        self.length += 5
        return bin_stream.to_int(content)

    def evaluate(self) -> int:
        return self.value


class OperatorPaquet(Paquet):
    OPERATORS = {
        0: lambda *args: sum(args),
        1: lambda *args: reduce(lambda memo, v: memo * v, args, 1),
        2: lambda *args: min(args),
        3: lambda *args: max(args),
        5: lambda left, right: left > right,
        6: lambda left, right: left < right,
        7: lambda left, right: left == right
    }

    def __init__(self, version, paquet_type):
        super().__init__(version, paquet_type)

    def parse(self, bin_stream: BinStream):
        length_id = bin_stream.next_as_int()
        if length_id:
            n_paquets = bin_stream.next_as_int(11)
            self.length += 12
            return self.get_n_paquets(n_paquets, bin_stream)
        else:
            paquet_length = bin_stream.next_as_int(15)
            self.length += 16
            return self.get_paquets_by_length(paquet_length, bin_stream)

    def get_n_paquets(self, n, bin_stream: BinStream):
        if n <= 0:
            return []
        next_paquet = self.parse_paquet_hierarchy(bin_stream)
        self.length += next_paquet.length
        return [next_paquet, *self.get_n_paquets(n - 1, bin_stream)]

    def get_paquets_by_length(self, length, bin_stream):
        if length <= 0:
            return []
        next_paquet = self.parse_paquet_hierarchy(bin_stream)
        self.length += next_paquet.length
        return [next_paquet, *self.get_paquets_by_length(length - next_paquet.length, bin_stream)]

    def evaluate(self) -> int:
        return self.OPERATORS[self.paquet_type](*[succ.evaluate() for succ in self.successors])


def solve1():
    bin_stream = BinStream(open('input.txt').readline().strip())
    return Paquet.parse_paquet_hierarchy(bin_stream).sum_versions()


def solve2():
    bin_stream = BinStream(open('input.txt').readline().strip())
    return Paquet.parse_paquet_hierarchy(bin_stream).evaluate()


print(solve1())
print(solve2())
