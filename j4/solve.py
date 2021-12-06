from collections import defaultdict
from typing import NamedTuple, Dict, Set, List

Position = NamedTuple('Position', [('r', int), ('c', int)])


def lines():
    for l in open("input.txt"):
        yield l


def row(li: str, split=None):
    return [int(n) for n in li.strip().split(split)]


class Board:

    def __init__(self):
        self.numbers: Dict[int, Position] = dict()
        self.columns: Dict[int, Set[int]] = defaultdict(set)
        self.rows: Dict[int, Set[int]] = defaultdict(set)
        self.bingo = False

    def add_number(self, n, r, c):
        self.numbers[n] = Position(r, c)
        self.columns[c].add(n)
        self.rows[r].add(n)

    def mark_number(self, n):
        r, c = self.numbers.pop(n)
        self.columns[c].remove(n)
        self.rows[r].remove(n)
        return len(self.columns[c]) == 0 or len(self.rows[r]) == 0

    def has_number(self, n):
        return n in self.numbers

    def all_unmarked(self) -> List[int]:
        return [v for s in self.columns.values() for v in s]


def build_boards():
    boards = []
    try:
        while True:
            line = next(line_reader)
            r = 0
            new_board = Board()
            boards.append(new_board)
            while line.strip() != '':
                for c, n in enumerate(row(line)):
                    new_board.add_number(n, r, c)
                line = next(line_reader)
                r += 1
    except StopIteration:
        return boards


def win_bingo(boards, randoms) -> (Board, int):
    for rand in randoms:
        for board in boards:
            if board.has_number(rand):
                board.bingo = board.mark_number(rand)
        if any(board.bingo for board in boards):
            return rand


def loose_bingo(boards: List[Board], randoms) -> (Board, int):
    while len(boards) > 1:
        last_draw = win_bingo(boards, randoms)
        for board in boards:
            if board.bingo:
                boards.remove(board)
        randoms = randoms[randoms.index(last_draw) + 1:]
    return win_bingo(boards, randoms)


line_reader = lines()
randoms = row(next(line_reader), split=',')
next(line_reader)
boards = build_boards()


def part1():
    last_draw = win_bingo(boards, randoms)
    winnning_board = next(board for board in boards if board.bingo)
    print(sum(winnning_board.all_unmarked()) * last_draw)


def part2():
    last_draw = loose_bingo(boards, randoms)
    print(sum(boards[0].all_unmarked()) * last_draw)


part1()
part2()
